from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False
)


def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(reusable_oauth2)
) -> User:
    if token:
        payload = decode_access_token(token)
        if payload and "sub" in payload:
            user = db.query(User).filter(User.id == payload["sub"]).first()
            if user and user.is_active:
                return user

    # If demo mode is active and no valid token, fallback to the first active homeowner
    # to facilitate frictionless demo integration for the local prototype
    if settings.DEMO_MODE:
        demo_user = db.query(User).filter(User.is_active == True).first()
        if demo_user:
            return demo_user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
