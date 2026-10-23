from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=120)
    password: str = Field(..., min_length=6, max_length=100)
    household_name: Optional[str] = "My Smart Home"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    household_id: Optional[str] = None
    role: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    household_id: str
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
