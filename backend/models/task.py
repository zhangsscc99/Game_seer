from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from core.database import Base


class TaskType(str, enum.Enum):
    daily = "daily"
    main = "main"
    challenge = "challenge"


class TaskCategory(str, enum.Enum):
    study = "study"
    work = "work"
    habit = "habit"
    health = "health"
    creative = "creative"


class TaskImportance(str, enum.Enum):
    normal = "normal"
    important = "important"
    critical = "critical"


class TaskStatus(str, enum.Enum):
    pending = "pending"
    done = "done"
    failed = "failed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(SAEnum(TaskType), default=TaskType.daily, nullable=False)
    category = Column(SAEnum(TaskCategory), default=TaskCategory.habit, nullable=False)
    difficulty = Column(Integer, default=1)  # 1-5
    duration = Column(Integer, default=30)   # minutes
    importance = Column(SAEnum(TaskImportance), default=TaskImportance.normal, nullable=False)
    status = Column(SAEnum(TaskStatus), default=TaskStatus.pending, nullable=False)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    exp_reward = Column(Integer, default=10)
    coins_reward = Column(Integer, default=5)

    user = relationship("User", back_populates="tasks")
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete-orphan")


class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exp_earned = Column(Integer, default=0)
    coins_earned = Column(Integer, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="logs")
    user = relationship("User", back_populates="task_logs")
