from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/")
def create_department(name: str, db: Session = Depends(get_db)):
    dept = models.Department(name=name)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

@router.get("/")
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()
