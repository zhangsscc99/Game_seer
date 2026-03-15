from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    task_logs = relationship("TaskLog", back_populates="user", cascade="all, delete-orphan")
    elves = relationship("UserElf", back_populates="user", cascade="all, delete-orphan")
    boss_records = relationship("UserBoss", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_active_date = Column(DateTime, nullable=True)
    total_tasks_completed = Column(Integer, default=0)
    unlock_credits = Column(Integer, default=0)   # 可用解锁额度
    title = Column(String, default="新手训练师")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profile")
