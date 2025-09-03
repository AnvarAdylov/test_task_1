from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
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
