from datetime import datetime, date
from sqlalchemy.orm import Session

from models.user import UserProfile


def update_streak(user_id: int, db: Session) -> int:
    """
    Update the user's streak days based on activity.
    - If last_active_date is today, do nothing (already counted).
    - If last_active_date was yesterday, increment streak.
    - Otherwise, reset streak to 1.
    Returns the current streak days.
    """
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        return 0

    today = date.today()
    last_active = profile.last_active_date.date() if profile.last_active_date else None

    if last_active == today:
        # Already updated today, no change
        return profile.streak_days

    if last_active is not None:
        delta = (today - last_active).days
        if delta == 1:
            # Consecutive day
            profile.streak_days += 1
        else:
            # Streak broken
            profile.streak_days = 1
    else:
        # First activity ever
        profile.streak_days = 1

    profile.last_active_date = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    return profile.streak_days
