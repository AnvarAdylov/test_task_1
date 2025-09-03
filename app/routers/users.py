from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user, require_roles
from app.core.security import hash_password
from app.db import get_db
from app.models import User
from app.schemas.users import UserCreate, UserRead, UserUpdateRole

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserRead,
    dependencies=[Depends(require_roles("ADMIN"))],
)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    # unique username check
    q = await db.execute(select(User).where(User.username == payload.username))
    if q.scalar_one_or_none():
        raise HTTPException(400, "Username already exists")

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=payload.role,
        department_id=payload.department_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get(
    "/",
    response_model=list[UserRead],
    dependencies=[Depends(require_roles("ADMIN", "MANAGER"))],
)
async def list_users(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User))
    return list(res.scalars().all())


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user),
):
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")

    if current.role in ("ADMIN", "MANAGER") or current.id == user_id:
        return user
    raise HTTPException(403, "Forbidden")


@router.put(
    "/{user_id}/role",
    response_model=UserRead,
    dependencies=[Depends(require_roles("ADMIN"))],
)
async def update_role(
    user_id: int, payload: UserUpdateRole, db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    user.role = payload.role
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", dependencies=[Depends(require_roles("ADMIN"))])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
    return {"ok": True}
