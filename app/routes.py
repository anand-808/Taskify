from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from bson import ObjectId
from datetime import datetime, timezone
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate, TaskStatus
from app.database import tasks_collection


router=APIRouter(
    prefix="/task",
    tags=["tasks"]
)


def task_helper(task) -> dict:
    """Helper function to convert MongoDB document to dict"""
    # Add status validation here
    raw_status = task.get("status", "pending")
    
    # Ensure status is valid, fallback to pending if not
    try:
        validated_status = TaskStatus(raw_status)
    except ValueError:
        validated_status = TaskStatus.PENDING
    
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description"),
        "status": validated_status.value,
        "created_at": task.get("created_at"),
        "updated_at": task.get("updated_at")
    }


def validate_object_id(id:str) -> ObjectId:
    """Validate and convert string ID to ObjectId"""
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Create a new task"""
    current_time = datetime.now(timezone.utc)
    task_dict = task.model_dump()
    task_dict.update({
        "created_at": current_time,
        "updated_at": current_time,
    })

    result= await tasks_collection.insert_one(task_dict)
    new_task = await tasks_collection.find_one({"_id": result.inserted_id})

    return task_helper(new_task)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks():
    """Get all tasks"""
    tasks=[]
    async for task in tasks_collection.find():
        tasks.append(task_helper(task))
    return tasks


@router.get("/filter/{status}", response_model=List[TaskResponse])
async def filter_tasks(status: TaskStatus):
    """Filter tasks by status - only accepts valid TaskStatus enum values"""
    tasks = []
    async for task in tasks_collection.find({"status": status.value}):
        tasks.append(task_helper(task))
    return tasks


@router.get("/search", response_model=List[TaskResponse])
async def search_tasks(q: str = Query(..., min_length=1, description="Search query")):
    """Search tasks by title or description"""
    search_regex = {"$regex": q, "$options": "i"}  # Case-insensitive search
    query = {
        "$or": [
            {"title": search_regex},
            {"description": search_regex}
        ]
    }
    
    tasks = []
    async for task in tasks_collection.find(query):
        tasks.append(task_helper(task))
    
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No tasks found matching search query: '{q}'"
        )
    
    return tasks


@router.get("/{id}", response_model=TaskResponse)
async def get_task(id: str):
    """Get a task by ID"""
    object_id = validate_object_id(id)
    task = await tasks_collection.find_one({"_id": object_id})

    if task:
        return task_helper(task)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {id} not found"
    )


@router.patch("/{id}", response_model=TaskResponse)
async def update_task(id: str, task_update: TaskUpdate):
    """Partially update a task by ID"""
    object_id=validate_object_id(id)

    # Only update fields that are provided (not None)
    update_data = {k: v for k, v in task_update.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_data["updated_at"] = datetime.now(timezone.utc)

    result = await tasks_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {id} not found"
        )
    updated_task = await tasks_collection.find_one({"_id": object_id})
    return task_helper(updated_task)


@router.patch("/{id}/status", response_model=TaskResponse)
async def update_task_status(id: str, status_update: TaskStatusUpdate):
    """Update only the status of a task - convenient endpoint for status changes"""
    object_id = validate_object_id(id)
    
    update_data = {
        "status": status_update.status,
        "updated_at": datetime.now(timezone.utc)
    }

    result = await tasks_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {id} not found"
        )
    
    updated_task = await tasks_collection.find_one({"_id": object_id})
    return task_helper(updated_task)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: str):
    """Delete a task by ID"""
    object_id = validate_object_id(id)
    
    result = await tasks_collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {id} not found"
        )
    
    return None