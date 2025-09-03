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
    type = Column(String, nullable=False)
    visibility = Column(
        Enum(Visibility), default=Visibility.PRIVATE, nullable=False
    )

    owner_id = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))

    file_metadata = Column(JSON, nullable=True)
    download_count = Column(Integer, default=0)

    owner = relationship("User", back_populates="files")
    department = relationship("Department")
