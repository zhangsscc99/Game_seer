from typing import List
from datetime import datetime

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
    """Get all achievements with user unlock status."""
    all_achievements = db.query(Achievement).order_by(Achievement.condition_value).all()
    user_unlocked = {
        ua.achievement_id: ua.earned_at
        for ua in db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).all()
    }
    result = []
    for a in all_achievements:
        data = {c.name: getattr(a, c.name) for c in a.__table__.columns}
        data["reward_elf"] = a.reward_elf
        data["unlocked"] = a.id in user_unlocked
        data["earned_at"] = user_unlocked.get(a.id)
        result.append(data)
    return result
