from pydantic import BaseModel, Field
from typing import Optional, Literal

Role = Literal["USER", "MANAGER", "ADMIN"]

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6)
    role: Role = "USER"
    department_id: Optional[int] = None

class UserRead(BaseModel):
    id: int
    username: str
    role: Role
    department_id: Optional[int]

    class Config:
        from_attributes = True

class UserUpdateRole(BaseModel):
    role: Role

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
