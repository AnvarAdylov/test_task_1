from datetime import datetime, timedelta, timezone
from typing import Optional  # noqa: F401

from fastapi import Depends, HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.core.auth import get_current_user
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admins only"
        )
    return current_user


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def create_access_token(
    data: dict, expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
