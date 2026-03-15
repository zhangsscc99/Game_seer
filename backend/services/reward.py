from typing import Dict
from sqlalchemy.orm import Session

from models.task import Task, TaskImportance
from models.user import UserProfile

# Importance multipliers for reward calculation
IMPORTANCE_MULTIPLIERS: Dict[str, float] = {
    TaskImportance.normal: 1.0,
    TaskImportance.important: 1.5,
    TaskImportance.critical: 2.0,
}

# Base exp/coins per difficulty point
BASE_EXP_PER_DIFFICULTY = 10
BASE_COINS_PER_DIFFICULTY = 5

# EXP required to level up: level * 100
EXP_PER_LEVEL = 100


def calculate_task_reward(task: Task) -> Dict[str, int]:
    """Calculate exp and coins reward for a task based on difficulty and importance."""
    multiplier = IMPORTANCE_MULTIPLIERS.get(task.importance, 1.0)
    exp = int(task.difficulty * BASE_EXP_PER_DIFFICULTY * multiplier)
    coins = int(task.difficulty * BASE_COINS_PER_DIFFICULTY * multiplier)
    return {"exp": exp, "coins": coins}


def apply_reward(user_id: int, exp: int, coins: int, db: Session) -> Dict:
    """
    Apply exp and coins to the user's profile.
    Handles level-up logic.
    Returns a dict with level_up flag and new level if leveled up.
    """
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        return {"level_up": False, "new_level": None}

    old_level = profile.level
    profile.exp += exp
    profile.coins += coins
    profile.total_tasks_completed += 1
    profile.unlock_credits += 1   # 每完成1个任务 +1 解锁额度

    # Level up logic: each level requires level * EXP_PER_LEVEL exp
    leveled_up = False
    while True:
        exp_needed = profile.level * EXP_PER_LEVEL
        if profile.exp >= exp_needed:
            profile.exp -= exp_needed
            profile.level += 1
            leveled_up = True
        else:
            break

    db.commit()
    db.refresh(profile)

    return {
        "level_up": leveled_up,
        "new_level": profile.level if leveled_up else None,
        "old_level": old_level,
    }
