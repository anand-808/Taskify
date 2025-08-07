from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    status: str = Field(default="pending", description="Task status")

class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass

class TaskUpdate(TaskBase):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    status: Optional[str] = Field(None, description="Task status")

class TaskResponse(TaskBase):
    """Schema for task response"""
    id: str = Field(..., description="Task ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
   
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
