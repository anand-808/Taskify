from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TaskStatus(str,Enum):
    """Allowed task status values"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    
class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating an existing task - all fields optional for partial updates"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")

class TaskStatusUpdate(BaseModel):
    """Schema for updating only the task status"""
    status: TaskStatus = Field(..., description="New task status")

class TaskResponse(TaskBase):
    """Schema for task response"""
    id: str = Field(..., description="Task ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
   
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    