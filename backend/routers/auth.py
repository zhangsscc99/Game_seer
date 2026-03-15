from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from core.config import settings
from models.user import User, UserProfile
from schemas.user import UserCreate, UserWithProfileResponse, Token
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserWithProfileResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check for existing email
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Check for existing username
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.flush()  # Get the new_user.id before committing

    profile = UserProfile(user_id=new_user.id)
    db.add(profile)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.email == login_data.email) | (User.username == login_data.email)
    ).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserWithProfileResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
