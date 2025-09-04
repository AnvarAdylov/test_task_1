from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel

Visibility = Literal["PRIVATE", "DEPARTMENT", "PUBLIC"]


class FileCreate(BaseModel):
    visibility: Visibility = "PRIVATE"


class FileRead(BaseModel):
    id: int
    filename: str
    owner_id: int
    department_id: Optional[int]
    visibility: Visibility
    meta: Optional[Dict[str, Any]] = None
    size: int
    mime_type: str
    download_count: int

    class Config:
        from_attributes = True
