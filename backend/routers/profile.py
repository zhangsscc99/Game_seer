from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database import get_db
from core.security import get_current_user
from models.user import User, UserProfile
from models.task import Task, TaskLog, TaskStatus, TaskCategory
from schemas.user import UserWithProfileResponse, UserProfileResponse

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/", response_model=UserWithProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current user's full profile including level, exp, coins, and streak."""
    return current_user


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get task statistics for the current user."""
    total_tasks = db.query(func.count(Task.id)).filter(Task.user_id == current_user.id).scalar()
    completed_tasks = (
        db.query(func.count(Task.id))
        .filter(Task.user_id == current_user.id, Task.status == TaskStatus.done)
        .scalar()
    )
    pending_tasks = (
        db.query(func.count(Task.id))
        .filter(Task.user_id == current_user.id, Task.status == TaskStatus.pending)
        .scalar()
    )
    failed_tasks = (
        db.query(func.count(Task.id))
        .filter(Task.user_id == current_user.id, Task.status == TaskStatus.failed)
        .scalar()
    )

    # Tasks by category
    category_counts = (
        db.query(Task.category, func.count(Task.id))
        .filter(Task.user_id == current_user.id, Task.status == TaskStatus.done)
        .group_by(Task.category)
        .all()
    )
    by_category = {str(cat): count for cat, count in category_counts}

    # Total exp and coins earned from logs
    total_exp_earned = (
        db.query(func.sum(TaskLog.exp_earned))
        .filter(TaskLog.user_id == current_user.id)
        .scalar()
        or 0
    )
    total_coins_earned = (
        db.query(func.sum(TaskLog.coins_earned))
        .filter(TaskLog.user_id == current_user.id)
        .scalar()
        or 0
    )

    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    streak_days = profile.streak_days if profile else 0

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "failed_tasks": failed_tasks,
        "completion_rate": round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0.0,
        "by_category": by_category,
        "total_exp_earned": total_exp_earned,
        "total_coins_earned": total_coins_earned,
        "streak_days": streak_days,
    }
