from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/users", tags=["Users"])

# Create user
@router.post("/")
def create_user(username: str, password_hash: str, role: str, department_id: int, db: Session = Depends(get_db)):
    new_user = models.User(
        username=username,
        password_hash=password_hash,
        role=role,
        department_id=department_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# List users
@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Get by id
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}
