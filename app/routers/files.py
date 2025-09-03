from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as Upload, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, or_, and_
from app.db import get_db
from app.models import File as FileModel, User
from app.schemas.files import FileCreate, FileRead
from app.core.auth import get_current_user
from app.services.storage import get_minio, ensure_bucket
from app.config import settings

router = APIRouter(prefix="/files", tags=["Files"])

MAX_SIZE = {
    "USER": 10 * 1024 * 1024,
    "MANAGER": 50 * 1024 * 1024,
    "ADMIN": 100 * 1024 * 1024,
}
PDF_ONLY_FOR_USER = True

def can_create_visibility(role: str, vis: str) -> bool:
    if role == "USER":
        return vis == "PRIVATE"
    return True  # manager/admin any

def can_view(user: User, f: FileModel) -> bool:
    if user.role == "ADMIN":
        return True
    if f.visibility == "PUBLIC":
        return True
    if f.visibility == "PRIVATE":
        return f.owner_id == user.id
    # DEPARTMENT visibility
    if user.role in ("MANAGER",) and user.department_id is not None:
        # managers can see all departments per spec? (stated: managers see all depts)
        return True
    return (user.department_id is not None) and (f.department_id == user.department_id)

def can_delete(user: User, f: FileModel) -> bool:
    if user.role == "ADMIN":
        return True
    if f.owner_id == user.id:
        return True
    if user.role == "MANAGER" and user.department_id and user.department_id == f.department_id:
        return True
    return False

@router.post("/upload", response_model=FileRead, status_code=201)
async def upload_file(
    meta: FileCreate,
    uploaded: UploadFile = Upload(...),
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    # role-based size/type limits
    content = await uploaded.read()
    size = len(content)
    if size > MAX_SIZE[current.role]:
        raise HTTPException(413, "File too large for your role")

    if current.role == "USER" and PDF_ONLY_FOR_USER:
        if uploaded.content_type not in ("application/pdf",):
            raise HTTPException(415, "USER role can upload only PDF")

    if not can_create_visibility(current.role, meta.visibility):
        raise HTTPException(403, "You cannot create files with this visibility")

    # store to MinIO
    client = get_minio()
    ensure_bucket(client, settings.S3_BUCKET)
    object_name = uploaded.filename  # could be made unique with UUID
    try:
        client.put_object(
            settings.S3_BUCKET,
            object_name,
            io.BytesIO(content),
            length=size,
            content_type=uploaded.content_type or "application/octet-stream",
        )
    except Exception as e:
        raise HTTPException(500, f"Storage error: {e}")

    f = FileModel(
        filename=object_name,
        owner_id=current.id,
        department_id=current.department_id,
        visibility=meta.visibility,
        meta={},  # metadata extraction will be via Celery later
        size=size,
        mime_type=uploaded.content_type or "application/octet-stream",
        download_count=0,
    )
    db.add(f)
    await db.commit()
    await db.refresh(f)
    return f

@router.get("/", response_model=list[FileRead])
async def list_files(db: AsyncSession = Depends(get_db), current: User = Depends(get_current_user)):
    # Managers see all departments per spec; admins everything; users: public + their dept + their own
    if current.role == "ADMIN":
        res = await db.execute(select(FileModel))
        return list(res.scalars().all())

    if current.role == "MANAGER":
        # managers see files of all departments (per spec)
        res = await db.execute(select(FileModel))
        return list(res.scalars().all())

    # USER
    res = await db.execute(
        select(FileModel).where(
            or_(
                FileModel.visibility == "PUBLIC",
                and_(
                    FileModel.visibility == "DEPARTMENT",
                    FileModel.department_id == current.department_id,
                ),
                FileModel.owner_id == current.id,
            )
        )
    )
    return list(res.scalars().all())

@router.get("/{file_id}", response_model=FileRead)
async def get_file(file_id: int, db: AsyncSession = Depends(get_db), current: User = Depends(get_current_user)):
    res = await db.execute(select(FileModel).where(FileModel.id == file_id))
    f = res.scalar_one_or_none()
    if not f:
        raise HTTPException(404, "File not found")
    if not can_view(current, f):
        raise HTTPException(403, "Forbidden")
    return f

@router.get("/{file_id}/download")
async def download_file(file_id: int, db: AsyncSession = Depends(get_db), current: User = Depends(get_current_user)):
    res = await db.execute(select(FileModel).where(FileModel.id == file_id))
    f = res.scalar_one_or_none()
    if not f:
        raise HTTPException(404, "File not found")
    if not can_view(current, f):
        raise HTTPException(403, "Forbidden")

    client = get_minio()
    try:
        # (option A) presigned URL
        url = client.presigned_get_object(settings.S3_BUCKET, f.filename)
    except Exception as e:
        raise HTTPException(500, f"Storage error: {e}")

    # increment download count
    f.download_count += 1
    await db.commit()
    return {"url": url}

@router.delete("/{file_id}")
async def delete_file(file_id: int, db: AsyncSession = Depends(get_db), current: User = Depends(get_current_user)):
    res = await db.execute(select(FileModel).where(FileModel.id == file_id))
    f = res.scalar_one_or_none()
    if not f:
        raise HTTPException(404, "File not found")
    if not can_delete(current, f):
        raise HTTPException(403, "Forbidden")

    client = get_minio()
    try:
        client.remove_object(settings.S3_BUCKET, f.filename)
    except Exception:
        # ignore missing object, proceed to delete DB record
        pass

    await db.execute(delete(FileModel).where(FileModel.id == file_id))
    await db.commit()
    return {"ok": True}
