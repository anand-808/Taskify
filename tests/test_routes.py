import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from bson import ObjectId
from app.schemas import TaskStatus
from datetime import datetime, timezone

class TestCreateTask:
    """Test POST /api/v1/task/"""
    
    @pytest.mark.asyncio
    async def test_create_task_success(self, async_client: AsyncClient, mock_tasks_collection, sample_task_response):
        """Test successful task creation"""
        # Create a sample response that matches our input
        custom_response = {
            "_id": sample_task_response["_id"],
            "title": "Test Task",
            "description": "Test description",
            "status": "pending",
            "created_at": sample_task_response["created_at"],
            "updated_at": sample_task_response["updated_at"]
        }
        
        # Mock database operations
        mock_tasks_collection.insert_one.return_value = AsyncMock(inserted_id=sample_task_response["_id"])
        mock_tasks_collection.find_one.return_value = custom_response
        
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "pending"
        }
        
        response = await async_client.post("/api/v1/task/", json=task_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test description"
        assert data["status"] == "pending"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    @pytest.mark.asyncio
    async def test_create_task_invalid_title(self, async_client: AsyncClient):
        """Test task creation with invalid title"""
        task_data = {
            "title": "",  # Empty title should fail
            "description": "Test description"
        }
        
        response = await async_client.post("/api/v1/task/", json=task_data)
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_create_task_invalid_status(self, async_client: AsyncClient):
        """Test task creation with invalid status"""
        task_data = {
            "title": "Test Task",
            "status": "invalid_status"
        }
        
        response = await async_client.post("/api/v1/task/", json=task_data)
        assert response.status_code == 422

class TestGetTasks:
    """Test GET /api/v1/task/"""
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_empty(self, async_client: AsyncClient, mock_tasks_collection):
        """Test getting all tasks when database is empty"""
        # Empty iterator is already set as default in fixture
        response = await async_client.get("/api/v1/task/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_with_data(self, async_client: AsyncClient, mock_tasks_collection, sample_task_response):
        """Test getting all tasks with data"""
        # Add data to mock collection instead of mocking find
        mock_tasks_collection._data = [sample_task_response]
        
        response = await async_client.get("/api/v1/task/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Task"

class TestGetTaskById:
    """Test GET /api/v1/task/{id}"""
    
    @pytest.mark.asyncio
    async def test_get_task_success(self, async_client: AsyncClient, mock_tasks_collection, sample_task_response, valid_object_id):
        """Test getting task by valid ID"""
        mock_tasks_collection.find_one.return_value = sample_task_response
        
        response = await async_client.get(f"/api/v1/task/{valid_object_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"
    
    @pytest.mark.asyncio
    async def test_get_task_not_found(self, async_client: AsyncClient, mock_tasks_collection, valid_object_id):
        """Test getting non-existent task"""
        mock_tasks_collection.find_one.return_value = None
        
        response = await async_client.get(f"/api/v1/task/{valid_object_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_get_task_invalid_id(self, async_client: AsyncClient, invalid_object_id):
        """Test getting task with invalid ID format"""
        response = await async_client.get(f"/api/v1/task/{invalid_object_id}")
        
        assert response.status_code == 400
        assert "Invalid task ID format" in response.json()["detail"]

class TestUpdateTask:
    """Test PATCH /api/v1/task/{id}"""
    
    @pytest.mark.asyncio
    async def test_update_task_success(self, async_client: AsyncClient, mock_tasks_collection, sample_task_response, valid_object_id):
        """Test successful task update"""
        # Mock successful update
        mock_tasks_collection.update_one.return_value = AsyncMock(matched_count=1)
        mock_tasks_collection.find_one.return_value = sample_task_response
        
        update_data = {"title": "Updated Title"}
        
        response = await async_client.patch(f"/api/v1/task/{valid_object_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_update_task_not_found(self, async_client: AsyncClient, mock_tasks_collection, valid_object_id):
        """Test updating non-existent task"""
        # Create a proper mock result object with matched_count=0
        class MockUpdateResult:
            def __init__(self):
                self.matched_count = 0
        
        mock_tasks_collection.update_one.return_value = MockUpdateResult()
        
        update_data = {"title": "Updated Title"}
        
        response = await async_client.patch(f"/api/v1/task/{valid_object_id}", json=update_data)
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_task_empty_data(self, async_client: AsyncClient, valid_object_id):
        """Test updating task with no data"""
        response = await async_client.patch(f"/api/v1/task/{valid_object_id}", json={})
        
        assert response.status_code == 400
        assert "No fields to update" in response.json()["detail"]

class TestUpdateTaskStatus:
    """Test PATCH /api/v1/task/{id}/status"""
    
    @pytest.mark.asyncio
    async def test_update_status_success(self, async_client: AsyncClient, mock_tasks_collection, sample_task_response, valid_object_id):
        """Test successful status update"""
        mock_tasks_collection.update_one.return_value = AsyncMock(matched_count=1)
        mock_tasks_collection.find_one.return_value = sample_task_response
        
        status_data = {"status": "completed"}
        
        response = await async_client.patch(f"/api/v1/task/{valid_object_id}/status", json=status_data)
        
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_update_status_invalid(self, async_client: AsyncClient, valid_object_id):
        """Test updating with invalid status"""
        status_data = {"status": "invalid_status"}
        
        response = await async_client.patch(f"/api/v1/task/{valid_object_id}/status", json=status_data)
        
        assert response.status_code == 422

class TestDeleteTask:
    """Test DELETE /api/v1/task/{id}"""
    
    @pytest.mark.asyncio
    async def test_delete_task_success(self, async_client: AsyncClient, mock_tasks_collection, valid_object_id):
        """Test successful task deletion"""
        mock_tasks_collection.delete_one.return_value = AsyncMock(deleted_count=1)
        
        response = await async_client.delete(f"/api/v1/task/{valid_object_id}")
        
        assert response.status_code == 204
    
    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, async_client: AsyncClient, mock_tasks_collection, valid_object_id):
        """Test deleting non-existent task"""
        # Create a proper mock result object with deleted_count=0
        class MockDeleteResult:
            def __init__(self):
                self.deleted_count = 0
        
        mock_tasks_collection.delete_one.return_value = MockDeleteResult()
        
        response = await async_client.delete(f"/api/v1/task/{valid_object_id}")
        
        assert response.status_code == 404

class TestFilterTasks:
    """Test GET /api/v1/task/filter/{status}"""
    
    @pytest.mark.asyncio
    async def test_filter_tasks_valid_status(self, async_client: AsyncClient, mock_tasks_collection, sample_task_response):
        """Test filtering with valid status"""
        # Add data to mock collection instead of mocking find
        mock_tasks_collection._data = [sample_task_response]
        
        response = await async_client.get("/api/v1/task/filter/pending")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    @pytest.mark.asyncio
    async def test_filter_tasks_invalid_status(self, async_client: AsyncClient):
        """Test filtering with invalid status"""
        response = await async_client.get("/api/v1/task/filter/invalid_status")
        
        assert response.status_code == 422

class TestSearchTasks:
    """Test GET /api/v1/task/search"""
    
    @pytest.mark.asyncio
    async def test_search_tasks_by_title(self, async_client: AsyncClient, mock_tasks_collection):
        """Test searching tasks by title"""
        # Create sample tasks with different titles
        search_results = [
            {
                "_id": ObjectId(),
                "title": "Python Development Task",
                "description": "Working on backend API",
                "status": "pending",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            },
            {
                "_id": ObjectId(),
                "title": "Python Testing Setup",
                "description": "Configure test environment",
                "status": "in_progress",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
        
        # Mock the find method to return search results
        async def search_iterator():
            for task in search_results:
                yield task
        
        mock_tasks_collection.find.return_value = search_iterator()
        
        response = await async_client.get("/api/v1/task/search?q=Python")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Python Development Task"
        assert data[1]["title"] == "Python Testing Setup"
    
    @pytest.mark.asyncio
    async def test_search_tasks_by_description(self, async_client: AsyncClient, mock_tasks_collection):
        """Test searching tasks by description"""
        search_results = [
            {
                "_id": ObjectId(),
                "title": "Backend Work",
                "description": "FastAPI development and testing",
                "status": "pending",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
        
        async def search_iterator():
            for task in search_results:
                yield task
        
        mock_tasks_collection.find.return_value = search_iterator()
        
        response = await async_client.get("/api/v1/task/search?q=FastAPI")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["description"] == "FastAPI development and testing"
    
    @pytest.mark.asyncio
    async def test_search_tasks_case_insensitive(self, async_client: AsyncClient, mock_tasks_collection):
        """Test that search is case-insensitive"""
        search_results = [
            {
                "_id": ObjectId(),
                "title": "JavaScript Frontend",
                "description": "React component development",
                "status": "completed",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
        
        async def search_iterator():
            for task in search_results:
                yield task
        
        mock_tasks_collection.find.return_value = search_iterator()
        
        # Test lowercase search for uppercase title
        response = await async_client.get("/api/v1/task/search?q=javascript")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "JavaScript Frontend"
    
    @pytest.mark.asyncio
    async def test_search_tasks_partial_match(self, async_client: AsyncClient, mock_tasks_collection):
        """Test partial string matching in search"""
        search_results = [
            {
                "_id": ObjectId(),
                "title": "Database Migration",
                "description": "Update database schema",
                "status": "pending",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
        
        async def search_iterator():
            for task in search_results:
                yield task
        
        mock_tasks_collection.find.return_value = search_iterator()
        
        # Search for partial word "data" should match "Database"
        response = await async_client.get("/api/v1/task/search?q=data")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Database" in data[0]["title"]
    
    @pytest.mark.asyncio
    async def test_search_tasks_no_results(self, async_client: AsyncClient, mock_tasks_collection):
        """Test search with no matching results"""
        # Mock empty search results
        async def empty_search_iterator():
            return
            yield  # This line will never be reached, making it an empty async iterator
        
        mock_tasks_collection.find.return_value = empty_search_iterator()
        
        response = await async_client.get("/api/v1/task/search?q=nonexistent")
        
        # Should return 404 when no tasks are found
        assert response.status_code == 404
        error_detail = response.json()
        assert "detail" in error_detail
        assert "No tasks found matching search query" in error_detail["detail"]
    
    @pytest.mark.asyncio
    async def test_search_tasks_multiple_matches_title_and_description(self, async_client: AsyncClient, mock_tasks_collection):
        """Test search that matches both title and description across different tasks"""
        search_results = [
            {
                "_id": ObjectId(),
                "title": "API Documentation",
                "description": "Write comprehensive docs",
                "status": "pending",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            },
            {
                "_id": ObjectId(),
                "title": "Setup Project",
                "description": "API development environment setup",
                "status": "completed",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
        
        async def search_iterator():
            for task in search_results:
                yield task
        
        mock_tasks_collection.find.return_value = search_iterator()
        
        # Search for "API" should match both tasks (title in first, description in second)
        response = await async_client.get("/api/v1/task/search?q=API")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        
        # Verify both tasks are returned
        titles = [task["title"] for task in data]
        assert "API Documentation" in titles
        assert "Setup Project" in titles
    
    @pytest.mark.asyncio
    async def test_search_tasks_empty_query_validation(self, async_client: AsyncClient):
        """Test that empty search query is rejected"""
        response = await async_client.get("/api/v1/task/search?q=")
        
        # FastAPI returns 422 for query validation errors
        assert response.status_code == 422
        error_detail = response.json()
        assert "detail" in error_detail
    
    @pytest.mark.asyncio
    async def test_search_tasks_missing_query_parameter(self, async_client: AsyncClient):
        """Test that missing query parameter is rejected"""
        response = await async_client.get("/api/v1/task/search")
        
        # FastAPI returns 422 for missing required query parameters
        assert response.status_code == 422
        error_detail = response.json()
        assert "detail" in error_detail
    
    @pytest.mark.asyncio
    async def test_search_tasks_whitespace_only_query(self, async_client: AsyncClient):
        """Test that whitespace-only query returns 404 when no results found"""
        response = await async_client.get("/api/v1/task/search?q=%20%20%20")  # URL encoded spaces
        
        # Whitespace-only queries should return 404 when no tasks match
        assert response.status_code == 404
        error_detail = response.json()
        assert "detail" in error_detail
        assert "No tasks found matching search query" in error_detail["detail"]
    
    @pytest.mark.asyncio
    async def test_search_tasks_special_characters(self, async_client: AsyncClient, mock_tasks_collection):
        """Test search with special characters"""
        search_results = [
            {
                "_id": ObjectId(),
                "title": "Fix bug #123",
                "description": "Resolve issue with user authentication",
                "status": "in_progress",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
        ]
        
        async def search_iterator():
            for task in search_results:
                yield task
        
        mock_tasks_collection.find.return_value = search_iterator()
        
        # Search for "#123" should work
        response = await async_client.get("/api/v1/task/search?q=%23123")  # URL encoded #123
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "#123" in data[0]["title"]