from fastapi import APIRouter, Depends, Path, status,Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.user import User
from app.utils.auth import get_current_user
from app.services.task_service import TaskService
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: Annotated[TaskCreate, Body(description="Task to be created")],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await TaskService.create_task(task, current_user, db)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await TaskService.get_tasks(current_user, db)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: Annotated[int,Path(title="user's post ID")],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await TaskService.get_task(task_id, current_user, db)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: Annotated[int,Path(title="user's post to be updated")],
    task_update: Annotated[TaskUpdate, Body(description="new task data, would be called for status only, but handled other thing fields just in case")],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await TaskService.update_task(task_id, task_update, current_user, db)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: Annotated[int,Path(title="user's post to be deleted")],
    current_user: Annotated[User ,Depends(get_current_user)],
    db: Annotated[AsyncSession,Depends(get_db)],
):
    return await TaskService.delete_task(task_id, current_user, db)
