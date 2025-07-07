from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task


class TaskService:
    @staticmethod
    async def create_task(task_create, current_user, db: AsyncSession):
        if task_create.status not in ["pending", "completed"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be 'pending' or 'completed'",
            )
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            status=task_create.status,
            user_id=current_user.id,
        )
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    @staticmethod
    async def get_tasks(current_user, db: AsyncSession):
        result = await db.execute(
            select(Task)
            .where(Task.user_id == current_user.id)
            .order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_task(task_id, current_user, db: AsyncSession):
        result = await db.execute(
            select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
        )
        task = result.scalars().first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        return task

    @staticmethod
    async def update_task(task_id, task_update, current_user, db: AsyncSession):
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

    @staticmethod
    async def delete_task(task_id, current_user, db: AsyncSession):
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
