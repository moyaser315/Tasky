from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: str
    status: str = "pending"  # "pending" or "completed"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    created_at: datetime
