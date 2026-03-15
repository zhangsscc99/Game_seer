from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    title: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    level: int
    exp: int
    coins: int
    streak_days: int
    last_active_date: Optional[datetime]
    total_tasks_completed: int
    unlock_credits: int = 0
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserWithProfileResponse(UserResponse):
    profile: Optional[UserProfileResponse] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
