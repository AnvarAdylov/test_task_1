from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str


class DepartmentRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DepartmentAssignUser(BaseModel):
    user_id: int


class DepartmentRemoveUser(BaseModel):
    user_id: int
