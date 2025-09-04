from typing import Optional

from pydantic import BaseModel, Field

from app.models.user import Role


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6)
    role: Role = Role.USER
    department_id: Optional[int] = None


class UserRead(BaseModel):
    id: int
    username: str
    role: Role
    department_id: Optional[int]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=64)
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[Role] = None
    department_id: Optional[int] = None


class UserUpdateRole(BaseModel):
    role: Role


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
