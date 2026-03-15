from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from models.boss import Boss, UserBoss, BossStatus
from models.user import User, UserProfile
from models.elf import UserElf
from models.achievement import Achievement, UserAchievement, ConditionType
from services.reward import apply_reward


def check_and_unlock_achievements(user_id: int, db: Session):
    """Check boss_defeat achievements and unlock any newly earned ones."""
    defeated_count = (
        db.query(UserBoss)
        .filter(UserBoss.user_id == user_id, UserBoss.status == BossStatus.defeated)
        .count()
    )
    boss_achievements = (
        db.query(Achievement)
        .filter(Achievement.condition_type == ConditionType.boss_defeat)
        .all()
    )
    already_unlocked = {
        ua.achievement_id
        for ua in db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()
    }
    newly_unlocked = []
    for ach in boss_achievements:
        if ach.id not in already_unlocked and defeated_count >= ach.condition_value:
            db.add(UserAchievement(user_id=user_id, achievement_id=ach.id))
            newly_unlocked.append(ach.name)
    if newly_unlocked:
        db.commit()
    return newly_unlocked


def get_or_create_user_boss(user_id: int, boss_id: int, db: Session) -> UserBoss:
    """Get existing UserBoss record or create a new locked one."""
    user_boss = (
        db.query(UserBoss)
        .filter(UserBoss.user_id == user_id, UserBoss.boss_id == boss_id)
        .first()
    )
    if not user_boss:
        user_boss = UserBoss(
            user_id=user_id,
            boss_id=boss_id,
            status=BossStatus.locked,
        )
        db.add(user_boss)
        db.commit()
        db.refresh(user_boss)
    return user_boss


def check_boss_availability(user_id: int, boss: Boss, db: Session) -> bool:
    """Check if the user has completed enough tasks to challenge the boss."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        return False
    return profile.total_tasks_completed >= boss.required_tasks


def challenge_boss(user_id: int, boss_id: int, db: Session) -> dict:
    """
    Challenge a boss. Checks conditions, applies rewards, unlocks elf if applicable.
    Returns a result dict.
    """
    boss = db.query(Boss).filter(Boss.id == boss_id).first()
    if not boss:
        return {"success": False, "message": "Boss not found", "exp_earned": 0, "coins_earned": 0}

    user_boss = get_or_create_user_boss(user_id, boss_id, db)

    # Check if already defeated and not repeatable
    if user_boss.status == BossStatus.defeated and not boss.is_repeatable:
        return {
            "success": False,
            "message": "Boss already defeated and is not repeatable",
            "exp_earned": 0,
            "coins_earned": 0,
        }

    # Check availability
    if not check_boss_availability(user_id, boss, db):
        return {
            "success": False,
            "message": f"Need to complete at least {boss.required_tasks} tasks to challenge this boss",
            "exp_earned": 0,
            "coins_earned": 0,
        }

    # Defeat the boss
    user_boss.status = BossStatus.defeated
    user_boss.defeated_at = datetime.utcnow()
    user_boss.defeat_count += 1
    db.commit()

    # Apply rewards
    apply_reward(user_id, boss.reward_exp, boss.reward_coins, db)

    # Unlock elf reward if applicable
    elf_unlocked = None
    if boss.reward_elf_id:
        existing_elf = (
            db.query(UserElf)
            .filter(UserElf.user_id == user_id, UserElf.template_id == boss.reward_elf_id)
            .first()
        )
        if not existing_elf:
            new_elf = UserElf(user_id=user_id, template_id=boss.reward_elf_id, level=1, exp=0, bond=0, is_active=False)
            db.add(new_elf)
            db.commit()
            elf_unlocked = boss.reward_elf

    # 检查并解锁成就
    check_and_unlock_achievements(user_id, db)

    db.refresh(user_boss)
    return {
        "success": True,
        "message": f"Boss '{boss.name}' defeated!",
        "exp_earned": boss.reward_exp,
        "coins_earned": boss.reward_coins,
        "elf_unlocked": elf_unlocked,
        "user_boss": user_boss,
    }
