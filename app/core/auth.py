from typing import Annotated, Callable, Literal

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        sub: str | None = payload.get("sub")
        if not sub:
            raise cred_exc
    except JWTError:
        raise cred_exc

    q = await db.execute(select(User).where(User.username == sub))
    user = q.scalar_one_or_none()
    if not user:
        raise cred_exc
    return user


Role = Literal["USER", "MANAGER", "ADMIN"]


def require_roles(*allowed: Role) -> Callable:
    async def _checker(
        current: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current.role not in allowed:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current

    return _checker
