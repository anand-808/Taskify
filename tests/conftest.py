import pytest
import asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock
from app.main import app
from app.database import tasks_collection
from app.schemas import TaskStatus
from bson import ObjectId
from datetime import datetime

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_tasks_collection(monkeypatch):
    """Mock the tasks collection for testing"""
    mock_collection = AsyncMock()
    monkeypatch.setattr("app.routes.tasks_collection", mock_collection)
    return mock_collection

@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "status": TaskStatus.PENDING
    }

@pytest.fixture
def sample_task_response():
    """Sample task response from database"""
    task_id = ObjectId()
    return {
        "_id": task_id,
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@pytest.fixture
def invalid_object_id():
    """Invalid ObjectId for testing"""
    return "invalid_id_format"

@pytest.fixture
def valid_object_id():
    """Valid ObjectId for testing"""
    return str(ObjectId())
