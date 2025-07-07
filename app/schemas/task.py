from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Annotated
from enum import Enum


class TaskStatus(str, Enum):

    PENDING = "pending"
    COMPLETED = "completed"



class TaskBase(BaseModel):
    title: Annotated[str, Field(description="Task title", min_length=1, max_length=200)]
    description: Annotated[str, Field(description="Task description", max_length=1000)]
    status: Annotated[TaskStatus, Field(default=TaskStatus.PENDING, description="Current task status")]


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Annotated[str | None, Field(None, description="Updated task title", min_length=1, max_length=200)]
    description: Annotated[str | None, Field(None, description="Updated task description", max_length=1000)]
    status: Annotated[TaskStatus | None, Field(None, description="Updated task status")]


class TaskResponse(TaskBase):
    """Schema for task response with database fields"""
    model_config = ConfigDict(from_attributes=True)
    
    id: Annotated[int, Field(description="Unique task identifier", gt=0)]
    user_id: Annotated[int, Field(description="ID of the user who owns this task", gt=0)]
    created_at: Annotated[datetime, Field(description="Timestamp when the task was created")]
