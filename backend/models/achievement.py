from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from core.database import Base


class ConditionType(str, enum.Enum):
    streak = "streak"
    total_tasks = "total_tasks"
    boss_defeat = "boss_defeat"
    elf_collect = "elf_collect"
    focus_time = "focus_time"


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    condition_type = Column(SAEnum(ConditionType), nullable=False)
    condition_value = Column(Integer, nullable=False)
    reward_elf_id = Column(Integer, ForeignKey("elf_templates.id"), nullable=True)
    reward_title = Column(String, nullable=True)

    reward_elf = relationship("ElfTemplate", foreign_keys=[reward_elf_id])
    user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
