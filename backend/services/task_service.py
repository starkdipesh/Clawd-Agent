from typing import List, Dict, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import uuid

class TaskService:
    def __init__(self, db):
        self.db = db
        self.tasks = db.tasks
    
    async def create_task(
        self, 
        user_id: str, 
        title: str, 
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: str = "medium",
        recurring: bool = False,
        recurrence_pattern: Optional[str] = None
    ) -> str:
        """Create a new task"""
        task = {
            "task_id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "status": "pending",
            "recurring": recurring,
            "recurrence_pattern": recurrence_pattern,
            "created_at": datetime.utcnow(),
            "completed_at": None
        }
        await self.tasks.insert_one(task)
        return task["task_id"]
    
    async def get_tasks(
        self, 
        user_id: str, 
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Dict]:
        """Get user's tasks with optional filters"""
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        if priority:
            query["priority"] = priority
        
        cursor = self.tasks.find(query).sort("due_date", 1)
        tasks = await cursor.to_list(length=100)
        return tasks
    
    async def get_upcoming_tasks(self, user_id: str, hours: int = 24) -> List[Dict]:
        """Get tasks due within specified hours"""
        now = datetime.utcnow()
        future = now + timedelta(hours=hours)
        
        cursor = self.tasks.find({
            "user_id": user_id,
            "status": "pending",
            "due_date": {"$gte": now, "$lte": future}
        }).sort("due_date", 1)
        
        tasks = await cursor.to_list(length=50)
        return tasks
    
    async def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed"""
        result = await self.tasks.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    async def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        result = await self.tasks.delete_one({"task_id": task_id})
        return result.deleted_count > 0
    
    async def update_task(self, task_id: str, updates: Dict) -> bool:
        """Update task fields"""
        result = await self.tasks.update_one(
            {"task_id": task_id},
            {"$set": updates}
        )
        return result.modified_count > 0