from fastapi import APIRouter, Depends, Path, status, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.user import User
from app.utils.auth import get_current_user
from app.services.task_service import TaskService
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/", 
    response_model=TaskResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user",
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid task data"},
        401: {"description": "Authentication required"}
    }
)
async def create_task(
    task: Annotated[TaskCreate, Body(description="Task data including title, description, and priority")],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """
    Create a new task for the authenticated user.
    
    - **title**: Task title 
    - **description**: Task description 
    - **status**: Task status 
    
    Returns the created task with its unique ID and timestamps.
    """
    return await TaskService.create_task(task, current_user, db)


@router.get(
    "/", 
    response_model=List[TaskResponse],
    summary="Get all user tasks",
    description="Retrieve all tasks belonging to the authenticated user",
    responses={
        200: {"description": "List of user tasks"},
        401: {"description": "Authentication required"}
    }
)
async def get_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> List[TaskResponse]:
    """
    Get all tasks for the authenticated user.
    
    Returns a list of all tasks created by the current user,
    ordered by creation date.
    """
    return await TaskService.get_tasks(current_user, db)


@router.get(
    "/{task_id}", 
    response_model=TaskResponse,
    summary="Get a specific task",
    description="Retrieve a specific task by its ID (must belong to authenticated user)",
    responses={
        200: {"description": "Task details"},
        401: {"description": "Authentication required"},
        403: {"description": "Access denied - task doesn't belong to user"},
        404: {"description": "Task not found"}
    }
)
async def get_task(
    task_id: Annotated[int, Path(description="The ID of the task to retrieve", gt=0)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """
    Get a specific task by ID.
    
    The task must belong to the authenticated user.
    Returns detailed task information including status and timestamps.
    """
    return await TaskService.get_task(task_id, current_user, db)


@router.put(
    "/{task_id}", 
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task (must belong to authenticated user)",
    responses={
        200: {"description": "Task updated successfully"},
        400: {"description": "Invalid update data"},
        401: {"description": "Authentication required"},
        403: {"description": "Access denied - task doesn't belong to user"},
        404: {"description": "Task not found"}
    }
)
async def update_task(
    task_id: Annotated[int, Path(description="The ID of the task to update", gt=0)],
    task_update: Annotated[
        TaskUpdate, 
        Body(description="Updated task data (only provided fields will be updated)")
    ],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    """
    Update an existing task.
    
    Only the fields provided in the request body will be updated.
    Common use case is updating the task status, but all fields
    can be modified if needed.
    
    The task must belong to the authenticated user.
    """
    return await TaskService.update_task(task_id, task_update, current_user, db)


@router.delete(
    "/{task_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete an existing task (must belong to authenticated user)",
    responses={
        204: {"description": "Task deleted successfully"},
        401: {"description": "Authentication required"},
        404: {"description": "Task not found"}
    }
)
async def delete_task(
    task_id: Annotated[int, Path(description="The ID of the task to delete", gt=0)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """
    Delete a task permanently.
    
    The task must belong to the authenticated user.
    This action cannot be undone.
    """
    return await TaskService.delete_task(task_id, current_user, db)