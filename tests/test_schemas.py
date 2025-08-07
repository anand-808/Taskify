import pytest
from pydantic import ValidationError
from app.schemas import (
    TaskCreate, TaskUpdate, TaskStatusUpdate, 
    TaskResponse, TaskStatus, TaskBase
)
from datetime import datetime

class TestTaskStatus:
    """Test TaskStatus enum"""
    
    def test_valid_status_values(self):
        """Test all valid status values"""
        assert TaskStatus.PENDING == "pending"
        assert TaskStatus.IN_PROGRESS == "in_progress"
        assert TaskStatus.COMPLETED == "completed"
        assert TaskStatus.CANCELLED == "cancelled"
    
    def test_invalid_status_value(self):
        """Test invalid status value raises error"""
        with pytest.raises(ValueError):
            TaskStatus("invalid_status")

class TestTaskCreate:
    """Test TaskCreate schema"""
    
    def test_valid_task_creation(self):
        """Test creating a valid task"""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": TaskStatus.PENDING
        }
        task = TaskCreate(**task_data)
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.PENDING
    
    def test_task_creation_with_defaults(self):
        """Test task creation with default values"""
        task = TaskCreate(title="Test Task")
        assert task.title == "Test Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING
    
    def test_invalid_title_too_short(self):
        """Test validation fails for empty title"""
        with pytest.raises(ValidationError):
            TaskCreate(title="")
    
    def test_invalid_title_too_long(self):
        """Test validation fails for title too long"""
        long_title = "x" * 101
        with pytest.raises(ValidationError):
            TaskCreate(title=long_title)
    
    def test_invalid_description_too_long(self):
        """Test validation fails for description too long"""
        long_description = "x" * 501
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", description=long_description)

class TestTaskUpdate:
    """Test TaskUpdate schema"""
    
    def test_empty_update(self):
        """Test empty update is valid"""
        update = TaskUpdate()
        assert update.title is None
        assert update.description is None
        assert update.status is None
    
    def test_partial_update(self):
        """Test partial update with only title"""
        update = TaskUpdate(title="Updated Title")
        assert update.title == "Updated Title"
        assert update.description is None
        assert update.status is None
    
    def test_status_only_update(self):
        """Test updating only status"""
        update = TaskUpdate(status=TaskStatus.COMPLETED)
        assert update.status == TaskStatus.COMPLETED
        assert update.title is None

class TestTaskStatusUpdate:
    """Test TaskStatusUpdate schema"""
    
    def test_valid_status_update(self):
        """Test valid status update"""
        status_update = TaskStatusUpdate(status=TaskStatus.COMPLETED)
        assert status_update.status == TaskStatus.COMPLETED
    
    def test_missing_status(self):
        """Test validation fails when status is missing"""
        with pytest.raises(ValidationError):
            TaskStatusUpdate()

class TestTaskResponse:
    """Test TaskResponse schema"""
    
    def test_valid_response(self):
        """Test valid task response"""
        response_data = {
            "id": "507f1f77bcf86cd799439011",
            "title": "Test Task",
            "description": "Test description",
            "status": TaskStatus.PENDING,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        response = TaskResponse(**response_data)
        assert response.id == "507f1f77bcf86cd799439011"
        assert response.title == "Test Task"