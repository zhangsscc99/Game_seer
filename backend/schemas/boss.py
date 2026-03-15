from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models.boss import BossType, BossStatus
from schemas.elf import ElfTemplateResponse


class BossCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None
    boss_type: BossType = BossType.daily
    required_tasks: int = 5
    reward_exp: int = 100
    reward_coins: int = 50
    reward_elf_id: Optional[int] = None
    is_repeatable: bool = False


class BossUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_path: Optional[str] = None
    required_tasks: Optional[int] = None
    reward_exp: Optional[int] = None
    reward_coins: Optional[int] = None
    reward_elf_id: Optional[int] = None
    is_repeatable: Optional[bool] = None


class BossResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    image_path: Optional[str]
    boss_type: BossType
    required_tasks: int
    reward_exp: int
    reward_coins: int
    reward_elf_id: Optional[int]
    is_repeatable: bool
    reward_elf: Optional[ElfTemplateResponse]

    class Config:
        from_attributes = True


class UserBossResponse(BaseModel):
    id: int
    user_id: int
    boss_id: int
    status: BossStatus
    defeated_at: Optional[datetime]
    defeat_count: int
    boss: BossResponse

    class Config:
        from_attributes = True


class BossChallengeResponse(BaseModel):
    success: bool
    message: str
    exp_earned: int
    coins_earned: int
    elf_unlocked: Optional[ElfTemplateResponse] = None
    user_boss: UserBossResponse
