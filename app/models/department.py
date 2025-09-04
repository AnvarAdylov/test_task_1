from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="department")
    files = relationship("File", back_populates="department")
