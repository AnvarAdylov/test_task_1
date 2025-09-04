import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Role(enum.Enum):
    USER = "USER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)

    department_id = Column(
        Integer, ForeignKey("departments.id"), nullable=True
    )

    # 🔗 Relationships
    department = relationship("Department", back_populates="users")
    files = relationship("File", back_populates="owner")
