from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.task import Task, TaskLog, TaskStatus, TaskType
from schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskCompleteResponse
from services.reward import calculate_task_reward, apply_reward
from services.streak import update_streak

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _get_task_or_404(task_id: int, user_id: int, db: Session) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    type: Optional[TaskType] = Query(None),
    task_status: Optional[TaskStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    if type:
        query = query.filter(Task.type == type)
    if task_status:
        query = query.filter(Task.status == task_status)
    return query.order_by(Task.created_at.desc()).all()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Auto-calculate rewards
    from models.task import TaskImportance
    from services.reward import IMPORTANCE_MULTIPLIERS, BASE_EXP_PER_DIFFICULTY, BASE_COINS_PER_DIFFICULTY

    multiplier = IMPORTANCE_MULTIPLIERS.get(task_data.importance, 1.0)
    exp_reward = int(task_data.difficulty * BASE_EXP_PER_DIFFICULTY * multiplier)
    coins_reward = int(task_data.difficulty * BASE_COINS_PER_DIFFICULTY * multiplier)

    new_task = Task(
        user_id=current_user.id,
        exp_reward=exp_reward,
        coins_reward=coins_reward,
        **task_data.model_dump(),
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = _get_task_or_404(task_id, current_user.id, db)

    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Recalculate rewards if difficulty or importance changed
    if "difficulty" in update_data or "importance" in update_data:
        from services.reward import IMPORTANCE_MULTIPLIERS, BASE_EXP_PER_DIFFICULTY, BASE_COINS_PER_DIFFICULTY
        multiplier = IMPORTANCE_MULTIPLIERS.get(task.importance, 1.0)
        task.exp_reward = int(task.difficulty * BASE_EXP_PER_DIFFICULTY * multiplier)
        task.coins_reward = int(task.difficulty * BASE_COINS_PER_DIFFICULTY * multiplier)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = _get_task_or_404(task_id, current_user.id, db)
    db.delete(task)
    db.commit()


@router.post("/{task_id}/complete", response_model=TaskCompleteResponse)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = _get_task_or_404(task_id, current_user.id, db)

    if task.status == TaskStatus.done:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task already completed",
        )

    rewards = calculate_task_reward(task)
    exp_earned = rewards["exp"]
    coins_earned = rewards["coins"]

    # Mark task as done
    task.status = TaskStatus.done
    task.completed_at = datetime.utcnow()
    # Update stored rewards in case they drifted
    task.exp_reward = exp_earned
    task.coins_reward = coins_earned
    db.flush()

    # Record the completion log
    log = TaskLog(
        task_id=task.id,
        user_id=current_user.id,
        exp_earned=exp_earned,
        coins_earned=coins_earned,
    )
    db.add(log)
    db.flush()

    # Apply rewards and update profile
    result = apply_reward(current_user.id, exp_earned, coins_earned, db)

    # Update streak
    update_streak(current_user.id, db)

    db.commit()
    db.refresh(task)
    db.refresh(log)

    return TaskCompleteResponse(
        task=task,
        log=log,
        exp_earned=exp_earned,
        coins_earned=coins_earned,
        level_up=result["level_up"],
        new_level=result.get("new_level"),
    )
