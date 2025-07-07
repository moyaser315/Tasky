from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.task import Task
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    if task.status not in ["pending", "completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'pending' or 'completed'",
        )

    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=current_user.id,
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    return db_task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    if task_update.title is not None:
        task.title = task_update.title

    if task_update.description is not None:
        task.description = task_update.description

    if task_update.status is not None:
        if task_update.status not in ["pending", "completed"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be 'pending' or 'completed'",
            )
        task.status = task_update.status

    await db.commit()
    await db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    await db.delete(task)
    await db.commit()

    return None
