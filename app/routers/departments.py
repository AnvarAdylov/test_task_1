from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import require_roles
from app.db import get_db
from app.models import Department, User
from app.schemas.departments import DepartmentCreate, DepartmentRead

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post(
    "/",
    response_model=DepartmentRead,
    dependencies=[Depends(require_roles("ADMIN"))],
)
async def create_department(
    payload: DepartmentCreate, db: AsyncSession = Depends(get_db)
):
    d = Department(name=payload.name)
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return d


@router.get(
    "/",
    response_model=list[DepartmentRead],
    dependencies=[Depends(require_roles("ADMIN", "MANAGER"))],
)
async def list_departments(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Department))
    return list(res.scalars().all())


@router.get(
    "/{dept_id}",
    response_model=DepartmentRead,
    dependencies=[Depends(require_roles("ADMIN", "MANAGER"))],
)
async def get_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    d = (
        await db.execute(select(Department).where(Department.id == dept_id))
    ).scalar_one_or_none()
    if not d:
        raise HTTPException(404, "Department not found")
    return d


@router.put(
    "/{dept_id}",
    response_model=DepartmentRead,
    dependencies=[Depends(require_roles("ADMIN"))],
)
async def update_department(
    dept_id: int, payload: DepartmentCreate, db: AsyncSession = Depends(get_db)
):
    d = (
        await db.execute(select(Department).where(Department.id == dept_id))
    ).scalar_one_or_none()
    if not d:
        raise HTTPException(404, "Department not found")

    d.name = payload.name
    await db.commit()
    await db.refresh(d)
    return d


@router.post(
    "/{dept_id}/assign/{user_id}",
    dependencies=[Depends(require_roles("ADMIN"))],
)
async def assign_user(
    dept_id: int, user_id: int, db: AsyncSession = Depends(get_db)
):
    d = (
        await db.execute(select(Department).where(Department.id == dept_id))
    ).scalar_one_or_none()
    if not d:
        raise HTTPException(404, "Department not found")
    u = (
        await db.execute(select(User).where(User.id == user_id))
    ).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    u.department_id = dept_id
    await db.commit()
    return {"ok": True}


@router.delete(
    "/{dept_id}/remove/{user_id}",
    dependencies=[Depends(require_roles("ADMIN"))],
)
async def remove_user(
    dept_id: int, user_id: int, db: AsyncSession = Depends(get_db)
):
    u = (
        await db.execute(select(User).where(User.id == user_id))
    ).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    if u.department_id != dept_id:
        raise HTTPException(400, "User is not in this department")
    u.department_id = None
    await db.commit()
    return {"ok": True}


@router.delete(
    "/{dept_id}",
    dependencies=[Depends(require_roles("ADMIN"))],
)
async def delete_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    d = (
        await db.execute(select(Department).where(Department.id == dept_id))
    ).scalar_one_or_none()
    if not d:
        raise HTTPException(404, "Department not found")

    res = await db.execute(select(User).where(User.department_id == dept_id))
    users = res.scalars().all()
    if users:
        raise HTTPException(
            400, "Cannot delete department with assigned users"
        )

    await db.execute(delete(Department).where(Department.id == dept_id))
    await db.commit()
    return {"detail": "Department deleted"}
