import pytest
import pytest_asyncio
import httpx
import asyncio
from unittest.mock import patch
from app.main import app
from app.schemas import TaskStatus
from bson import ObjectId
from datetime import datetime, timezone

@pytest_asyncio.fixture
async def async_client():
    """Create async test client"""
    from fastapi.testclient import TestClient
    from httpx import AsyncClient
    
    # Create transport that uses our FastAPI app
    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

class AsyncIteratorMock:
    """Helper class to mock async iterators for MongoDB find operations"""
    
    def __init__(self, items):
        self.items = items
        self.index = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        item = self.items[self.index]
        self.index += 1
        return item

class MockMethod:
    """Mock method that supports return_value assignment"""
    def __init__(self, method, method_name=None):
        self.method = method
        self.method_name = method_name
        self.return_value = None
        self.is_find_method = method_name == 'find'
    
    def __call__(self, *args, **kwargs):
        if self.return_value is not None:
            if hasattr(self.return_value, '__call__'):
                result = self.return_value(*args, **kwargs)
                return result
            return self.return_value
        
        # Call original method
        return self.method(*args, **kwargs)


class AsyncMockMethod:
    """Async mock method that supports return_value assignment"""
    def __init__(self, method, method_name=None):
        self.method = method
        self.method_name = method_name
        self.return_value = None
    
    async def __call__(self, *args, **kwargs):
        if self.return_value is not None:
            # If return_value is callable, call it
            if hasattr(self.return_value, '__call__'):
                result = self.return_value(*args, **kwargs)
                if hasattr(result, '__await__'):
                    return await result
                return result
            # If it's an AsyncMock or mock object, return it directly
            return self.return_value
        
        # Call original method
        return await self.method(*args, **kwargs)

class MockTasksCollection:
    """Mock MongoDB collection that supports both test data and return_value patterns"""
    
    def __init__(self):
        self._data = []
        self.insert_one = AsyncMockMethod(self._insert_one, 'insert_one')
        self.find_one = AsyncMockMethod(self._find_one, 'find_one')
        self.find = MockMethod(self._find, 'find')  # Sync method for async iteration
        self.update_one = AsyncMockMethod(self._update_one, 'update_one')
        self.delete_one = AsyncMockMethod(self._delete_one, 'delete_one')
    
    def reset(self):
        """Reset the mock for each test"""
        self._data = []
        self.insert_one.return_value = None
        self.find_one.return_value = None
        self.find.return_value = None
        self.update_one.return_value = None
        self.delete_one.return_value = None
    
    async def _insert_one(self, document):
        from unittest.mock import AsyncMock
        mock_result = AsyncMock()
        mock_result.inserted_id = ObjectId()
        return mock_result
    
    async def _find_one(self, query):
        return None
    
    def _find(self, query=None):
        return AsyncIteratorMock(self._data)
    
    async def _update_one(self, query, update):
        from unittest.mock import AsyncMock
        mock_result = AsyncMock()
        mock_result.matched_count = 1
        return mock_result
    
    async def _delete_one(self, query):
        from unittest.mock import AsyncMock
        mock_result = AsyncMock()
        mock_result.deleted_count = 1
        return mock_result

@pytest.fixture
def mock_tasks_collection():
    """Mock the tasks collection for testing"""
    mock_collection = MockTasksCollection()
    
    with patch("app.routes.tasks_collection", mock_collection):
        yield mock_collection
    
    # Reset after each test
    mock_collection.reset()

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
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }

@pytest.fixture
def invalid_object_id():
    """Invalid ObjectId for testing"""
    return "invalid_id_format"

@pytest.fixture
def valid_object_id():
    """Valid ObjectId for testing"""
    return str(ObjectId())