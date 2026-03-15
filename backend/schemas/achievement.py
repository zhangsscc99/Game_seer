from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models.achievement import ConditionType
from schemas.elf import ElfTemplateResponse


class AchievementCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    condition_type: ConditionType
    condition_value: int
    reward_elf_id: Optional[int] = None
    reward_title: Optional[str] = None


class AchievementUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    condition_value: Optional[int] = None
    reward_elf_id: Optional[int] = None
    reward_title: Optional[str] = None


class AchievementResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    condition_type: ConditionType
    condition_value: int
    reward_elf_id: Optional[int]
    reward_title: Optional[str]
    reward_elf: Optional[ElfTemplateResponse]

    class Config:
        from_attributes = True


class UserAchievementResponse(BaseModel):
    id: int
    user_id: int
    achievement_id: int
    earned_at: datetime
    achievement: AchievementResponse

    class Config:
        from_attributes = True
