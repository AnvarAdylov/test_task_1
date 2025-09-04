import enum

from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Visibility(enum.Enum):
    PRIVATE = "PRIVATE"
    DEPARTMENT = "DEPARTMENT"
    PUBLIC = "PUBLIC"


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)  # ✅ matches schema
    visibility = Column(
        Enum(Visibility), default=Visibility.PRIVATE, nullable=False
    )

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(
        Integer, ForeignKey("departments.id"), nullable=True
    )

    meta = Column(JSON, nullable=True)  # ✅ matches schema
    download_count = Column(Integer, default=0)

    # 🔗 Relationships
    owner = relationship("User", back_populates="files")
    department = relationship("Department", back_populates="files")
