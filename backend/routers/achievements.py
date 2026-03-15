from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.achievement import Achievement, UserAchievement
from schemas.achievement import AchievementResponse, UserAchievementResponse

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/", response_model=List[AchievementResponse])
def list_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all available achievements."""
    return db.query(Achievement).all()


@router.get("/my", response_model=List[UserAchievementResponse])
def get_my_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get achievements unlocked by the current user."""
    return (
        db.query(UserAchievement)
        .filter(UserAchievement.user_id == current_user.id)
        .order_by(UserAchievement.earned_at.desc())
        .all()
    )
