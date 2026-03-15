from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum, Boolean
from sqlalchemy.orm import relationship
import enum

from core.database import Base


class BossType(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    main = "main"


class BossStatus(str, enum.Enum):
    locked = "locked"
    available = "available"
    defeated = "defeated"


class Boss(Base):
    __tablename__ = "bosses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    boss_type = Column(SAEnum(BossType), default=BossType.daily, nullable=False)
    required_tasks = Column(Integer, default=5)
    reward_exp = Column(Integer, default=100)
    reward_coins = Column(Integer, default=50)
    reward_elf_id = Column(Integer, ForeignKey("elf_templates.id"), nullable=True)
    is_repeatable = Column(Boolean, default=False)

    reward_elf = relationship("ElfTemplate", foreign_keys=[reward_elf_id])
    user_records = relationship("UserBoss", back_populates="boss", cascade="all, delete-orphan")


class UserBoss(Base):
    __tablename__ = "user_bosses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    boss_id = Column(Integer, ForeignKey("bosses.id"), nullable=False)
    status = Column(SAEnum(BossStatus), default=BossStatus.locked, nullable=False)
    defeated_at = Column(DateTime, nullable=True)
    defeat_count = Column(Integer, default=0)

    user = relationship("User", back_populates="boss_records")
    boss = relationship("Boss", back_populates="user_records")
