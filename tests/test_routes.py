import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from bson import ObjectId
from datetime import datetime
from app.schemas import TaskStatus

class TestCreateTask:
    """Test POST /api/v1/task/"""
    
    @pytest.mark.asyncio
    async def test_create_task_success(self, client: AsyncClient, mock_tasks_collection, sample_task_response):
        """Test successful task creation"""
        # Mock database operations
        mock_tasks_collection.insert_one.return_value = AsyncMock(inserted_id=sample_task_response["_id"])
        mock_tasks_collection.find_one.return_value = sample_task_response
        
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "pending"
        }
        
        response = await client.post("/api/v1/task/", json=task_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test description"
        assert data["status"] == "pending"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    @pytest.mark.asyncio
    async def test_create_task_invalid_title(self, client: AsyncClient):
        """Test task creation with invalid title"""
        task_data = {
            "title": "",  # Empty title should fail
            "description": "Test description"
        }
        
        response = await client.post("/api/v1/task/", json=task_data)
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_create_task_invalid_status(self, client: AsyncClient):
        """Test task creation with invalid status"""
        task_data = {
            "title": "Test Task",
            "status": "invalid_status"
        }
        
        response = await client.post("/api/v1/task/", json=task_data)
        assert response.status_code == 422

class TestGetTasks:
    """Test GET /api/v1/task/"""
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_empty(self, client: AsyncClient, mock_tasks_collection):
        """Test getting all tasks when database is empty"""
        # Mock empty result
        mock_tasks_collection.find.return_value.__aiter__.return_value = []
        
        response = await client.get("/api/v1/task/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_with_data(self, client: AsyncClient, mock_tasks_collection, sample_task_response):
        """Test getting all tasks with data"""
        # Mock result with one task
        mock_tasks_collection.find.return_value.__aiter__.return_value = [sample_task_response]
        
        response = await client.get("/api/v1/task/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Task"

class TestGetTaskById:
    """Test GET /api/v1/task/{id}"""
    
    @pytest.mark.asyncio
    async def test_get_task_success(self, client: AsyncClient, mock_tasks_collection, sample_task_response, valid_object_id):
        """Test getting task by valid ID"""
        mock_tasks_collection.find_one.return_value = sample_task_response
        
        response = await client.get(f"/api/v1/task/{valid_object_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"
    
    @pytest.mark.asyncio
    async def test_get_task_not_found(self, client: AsyncClient, mock_tasks_collection, valid_object_id):
        """Test getting non-existent task"""
        mock_tasks_collection.find_one.return_value = None
        
        response = await client.get(f"/api/v1/task/{valid_object_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_get_task_invalid_id(self, client: AsyncClient, invalid_object_id):
        """Test getting task with invalid ID format"""
        response = await client.get(f"/api/v1/task/{invalid_object_id}")
        
        assert response.status_code == 400
        assert "Invalid task ID format" in response.json()["detail"]

class TestUpdateTask:
    """Test PATCH /api/v1/task/{id}"""
    
    @pytest.mark.asyncio
    async def test_update_task_success(self, client: AsyncClient, mock_tasks_collection, sample_task_response, valid_object_id):
        """Test successful task update"""
        # Mock successful update
        mock_tasks_collection.update_one.return_value = AsyncMock(matched_count=1)
        mock_tasks_collection.find_one.return_value = sample_task_response
        
        update_data = {"title": "Updated Title"}
        
        response = await client.patch(f"/api/v1/task/{valid_object_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_update_task_not_found(self, client: AsyncClient, mock_tasks_collection, valid_object_id):
        """Test updating non-existent task"""
        mock_tasks_collection.update_one.return_value = AsyncMock(matched_count=0)
        
        update_data = {"title": "Updated Title"}
        
        response = await client.patch(f"/api/v1/task/{valid_object_id}", json=update_data)
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_task_empty_data(self, client: AsyncClient, valid_object_id):
        """Test updating task with no data"""
        response = await client.patch(f"/api/v1/task/{valid_object_id}", json={})
        
        assert response.status_code == 400
        assert "No fields to update" in response.json()["detail"]

class TestUpdateTaskStatus:
    """Test PATCH /api/v1/task/{id}/status"""
    
    @pytest.mark.asyncio
    async def test_update_status_success(self, client: AsyncClient, mock_tasks_collection, sample_task_response, valid_object_id):
        """Test successful status update"""
        mock_tasks_collection.update_one.return_value = AsyncMock(matched_count=1)
        mock_tasks_collection.find_one.return_value = sample_task_response
        
        status_data = {"status": "completed"}
        
        response = await client.patch(f"/api/v1/task/{valid_object_id}/status", json=status_data)
        
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_update_status_invalid(self, client: AsyncClient, valid_object_id):
        """Test updating with invalid status"""
        status_data = {"status": "invalid_status"}
        
        response = await client.patch(f"/api/v1/task/{valid_object_id}/status", json=status_data)
        
        assert response.status_code == 422

class TestDeleteTask:
    """Test DELETE /api/v1/task/{id}"""
    
    @pytest.mark.asyncio
    async def test_delete_task_success(self, client: AsyncClient, mock_tasks_collection, valid_object_id):
        """Test successful task deletion"""
        mock_tasks_collection.delete_one.return_value = AsyncMock(deleted_count=1)
        
        response = await client.delete(f"/api/v1/task/{valid_object_id}")
        
        assert response.status_code == 204
    
    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, client: AsyncClient, mock_tasks_collection, valid_object_id):
        """Test deleting non-existent task"""
        mock_tasks_collection.delete_one.return_value = AsyncMock(deleted_count=0)
        
        response = await client.delete(f"/api/v1/task/{valid_object_id}")
        
        assert response.status_code == 404

class TestFilterTasks:
    """Test GET /api/v1/task/filter/{status}"""
    
    @pytest.mark.asyncio
    async def test_filter_tasks_valid_status(self, client: AsyncClient, mock_tasks_collection, sample_task_response):
        """Test filtering with valid status"""
        mock_tasks_collection.find.return_value.__aiter__.return_value = [sample_task_response]
        
        response = await client.get("/api/v1/task/filter/pending")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    @pytest.mark.asyncio
    async def test_filter_tasks_invalid_status(self, client: AsyncClient):
        """Test filtering with invalid status"""
        response = await client.get("/api/v1/task/filter/invalid_status")
        
        assert response.status_code == 422