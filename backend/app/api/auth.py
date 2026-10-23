import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    household_id = str(uuid.uuid4())
    user = User(
        household_id=household_id,
        full_name=user_in.full_name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role="homeowner",
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.id, household_id=user.household_id, role=user.role)
    return Token(access_token=token, token_type="bearer", user=UserResponse.model_validate(user))


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")

    token = create_access_token(subject=user.id, household_id=user.household_id, role=user.role)
    return Token(access_token=token, token_type="bearer", user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}
