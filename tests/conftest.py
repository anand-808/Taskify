import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock
from app.main import app
from app.database import tasks_collection
from app.schemas import TaskStatus
from bson import ObjectId
from datetime import datetime, timezone

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def async_client():
    """Create async test client"""
    from fastapi.testclient import TestClient
    from httpx import AsyncClient
    import httpx
    
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
    def __init__(self, method):
        self.method = method
        self.return_value = None
    
    async def __call__(self, *args, **kwargs):
        if self.return_value is not None:
            # If return value is already awaitable, return it directly
            if hasattr(self.return_value, '__await__'):
                return await self.return_value
            return self.return_value
        return await self.method(*args, **kwargs)

class MockTasksCollection:
    """Mock tasks collection that properly handles async iteration"""
    def __init__(self):
        self._data = []
        self.inserted_id = None
        self.modified_count = 0
        self.deleted_count = 0
        
        # Create mock method wrappers
        self.find_one = MockMethod(self._find_one)
        self.insert_one = MockMethod(self._insert_one)
        self.update_one = MockMethod(self._update_one)
        self.delete_one = MockMethod(self._delete_one)
    
    def find(self, filter=None):
        """Return async iterator mock"""
        if filter:
            # Simple filter simulation
            filtered_data = [item for item in self._data if self._matches_filter(item, filter)]
            return AsyncIteratorMock(filtered_data)
        return AsyncIteratorMock(self._data)
    
    async def _find_one(self, filter):
        """Find one document"""
        if isinstance(filter, dict) and "_id" in filter:
            for item in self._data:
                if item["_id"] == filter["_id"]:
                    return item
        return None
    
    async def _insert_one(self, document):
        """Insert one document"""
        doc_id = ObjectId()
        document["_id"] = doc_id
        self._data.append(document)
        result = AsyncMock()
        result.inserted_id = doc_id
        return result
    
    async def _update_one(self, filter, update):
        """Update one document"""
        modified_count = 0
        if isinstance(filter, dict) and "_id" in filter:
            for item in self._data:
                if item["_id"] == filter["_id"]:
                    if "$set" in update:
                        item.update(update["$set"])
                    modified_count = 1
                    break
        result = AsyncMock()
        result.modified_count = modified_count
        result.matched_count = modified_count  # Some tests expect this
        return result
    
    async def _delete_one(self, filter):
        """Delete one document"""
        deleted_count = 0
        if isinstance(filter, dict) and "_id" in filter:
            for i, item in enumerate(self._data):
                if item["_id"] == filter["_id"]:
                    del self._data[i]
                    deleted_count = 1
                    break
        result = AsyncMock()
        result.deleted_count = deleted_count
        return result
    
    def _matches_filter(self, item, filter):
        """Simple filter matching"""
        for key, value in filter.items():
            if key in item and item[key] != value:
                return False
        return True

# Global mock instance
mock_collection_instance = MockTasksCollection()

@pytest.fixture(autouse=True)
def mock_tasks_collection(monkeypatch):
    """Mock the tasks collection for testing"""
    # Reset the mock collection for each test
    mock_collection_instance._data = []
    mock_collection_instance.modified_count = 0
    mock_collection_instance.deleted_count = 0
    
    # Reset return values
    mock_collection_instance.find_one.return_value = None
    mock_collection_instance.insert_one.return_value = None
    mock_collection_instance.update_one.return_value = None
    mock_collection_instance.delete_one.return_value = None
    
    # Patch both possible import paths
    monkeypatch.setattr("app.database.tasks_collection", mock_collection_instance)
    monkeypatch.setattr("app.routes.tasks_collection", mock_collection_instance)
    
    return mock_collection_instance

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