from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    name: str

class DepartmentRead(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
