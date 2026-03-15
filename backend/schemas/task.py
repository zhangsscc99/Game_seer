from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

from models.task import TaskType, TaskCategory, TaskImportance, TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: TaskType = TaskType.daily
    category: TaskCategory = TaskCategory.habit
    difficulty: int = 1
    duration: int = 30
    importance: TaskImportance = TaskImportance.normal
    due_date: Optional[datetime] = None

    @validator("difficulty")
    def validate_difficulty(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("difficulty must be between 1 and 5")
        return v

    @validator("duration")
    def validate_duration(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("duration must be positive")
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[TaskType] = None
    category: Optional[TaskCategory] = None
    difficulty: Optional[int] = None
    duration: Optional[int] = None
    importance: Optional[TaskImportance] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    type: TaskType
    category: TaskCategory
    difficulty: int
    duration: int
    importance: TaskImportance
    status: TaskStatus
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    exp_reward: int
    coins_reward: int

    class Config:
        from_attributes = True


class TaskLogResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    exp_earned: int
    coins_earned: int
    completed_at: datetime

    class Config:
        from_attributes = True


class TaskCompleteResponse(BaseModel):
    task: TaskResponse
    log: TaskLogResponse
    exp_earned: int
    coins_earned: int
    level_up: bool
    new_level: Optional[int] = None
