from fastapi import APIRouter, HTTPException
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

def get_db():
    from server import db
    return db

class TaskCreate(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"
    recurring: bool = False
    recurrence_pattern: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None

@router.post("/create")
async def create_task(task: TaskCreate):
    """Create a new task"""
    try:
        db = get_db()
        task_service = TaskService(db)
        
        task_id = await task_service.create_task(
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            priority=task.priority,
            recurring=task.recurring,
            recurrence_pattern=task.recurrence_pattern
        )
        
        return {"success": True, "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{user_id}")
async def get_tasks(
    user_id: str,
    status: Optional[str] = None,
    priority: Optional[str] = None
):
    """Get user's tasks"""
    try:
        db = get_db()
        task_service = TaskService(db)
        
        tasks = await task_service.get_tasks(user_id, status, priority)
        
        # Remove MongoDB _id
        for task in tasks:
            task.pop("_id", None)
        
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/upcoming/{user_id}")
async def get_upcoming_tasks(user_id: str, hours: int = 24):
    """Get upcoming tasks"""
    try:
        db = get_db()
        task_service = TaskService(db)
        
        tasks = await task_service.get_upcoming_tasks(user_id, hours)
        
        for task in tasks:
            task.pop("_id", None)
        
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/complete/{task_id}")
async def complete_task(task_id: str):
    """Mark task as completed"""
    try:
        db = get_db()
        task_service = TaskService(db)
        
        success = await task_service.complete_task(task_id)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{task_id}")
async def update_task(task_id: str, update: TaskUpdate):
    """Update task fields"""
    try:
        db = get_db()
        task_service = TaskService(db)
        
        updates = {k: v for k, v in update.dict().items() if v is not None}
        success = await task_service.update_task(task_id, updates)
        
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    try:
        db = get_db()
        task_service = TaskService(db)
        
        success = await task_service.delete_task(task_id)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))