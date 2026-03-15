from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.boss import Boss, UserBoss, BossStatus
from schemas.boss import BossResponse, UserBossResponse, BossChallengeResponse
from services.boss import challenge_boss, get_or_create_user_boss

router = APIRouter(prefix="/boss", tags=["boss"])


@router.get("/", response_model=List[BossResponse])
def list_bosses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all bosses."""
    return db.query(Boss).all()


@router.get("/{boss_id}", response_model=BossResponse)
def get_boss(
    boss_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get details of a specific boss."""
    boss = db.query(Boss).filter(Boss.id == boss_id).first()
    if not boss:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Boss not found")
    return boss


@router.post("/{boss_id}/challenge", response_model=BossChallengeResponse)
def challenge_boss_route(
    boss_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Challenge a boss. Checks prerequisites and applies rewards on success."""
    boss = db.query(Boss).filter(Boss.id == boss_id).first()
    if not boss:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Boss not found")

    result = challenge_boss(current_user.id, boss_id, db)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"],
        )

    return BossChallengeResponse(
        success=result["success"],
        message=result["message"],
        exp_earned=result["exp_earned"],
        coins_earned=result["coins_earned"],
        elf_unlocked=result.get("elf_unlocked"),
        user_boss=result["user_boss"],
    )
