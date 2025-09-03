from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/files", tags=["Files"])

@router.get("/")
def list_files(db: Session = Depends(get_db)):
    return db.query(models.File).all()
