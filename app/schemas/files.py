from pydantic import BaseModel
from typing import Optional, Literal, Any

Visibility = Literal["PRIVATE", "DEPARTMENT", "PUBLIC"]

class FileCreate(BaseModel):
    visibility: Visibility

class FileRead(BaseModel):
    id: int
    filename: str
    owner_id: int
    department_id: Optional[int]
    visibility: Visibility
    meta: Optional[dict] = None
    size: int
    mime_type: str
    download_count: int
    class Config:
        from_attributes = True
