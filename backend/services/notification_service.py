from typing import List, Dict, Optional
from datetime import datetime, timedelta
import asyncio

class NotificationService:
    def __init__(self, db):
        self.db = db
        self.notifications = db.notifications
    
    async def create_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        notification_type: str = "info",
        data: Optional[Dict] = None,
        scheduled_for: Optional[datetime] = None
    ) -> str:
        """Create a notification"""
        notification = {
            "user_id": user_id,
            "title": title,
            "body": body,
            "type": notification_type,
            "data": data or {},
            "read": False,
            "sent": scheduled_for is None,
            "scheduled_for": scheduled_for,
            "created_at": datetime.utcnow()
        }
        result = await self.notifications.insert_one(notification)
        return str(result.inserted_id)
    
    async def get_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Dict]:
        """Get user notifications"""
        query = {"user_id": user_id}
        if unread_only:
            query["read"] = False
        
        cursor = self.notifications.find(query).sort("created_at", -1).limit(limit)
        notifications = await cursor.to_list(length=limit)
        return notifications
    
    async def mark_as_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        from bson import ObjectId
        result = await self.notifications.update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": {"read": True}}
        )
        return result.modified_count > 0
    
    async def send_daily_briefing(self, user_id: str, tasks: List[Dict], events: List[Dict]):
        """Send daily briefing notification"""
        task_count = len([t for t in tasks if t["status"] == "pending"])
        event_count = len(events)
        
        body = f"Good morning! You have {task_count} pending tasks and {event_count} events today."
        
        await self.create_notification(
            user_id=user_id,
            title="Daily Briefing",
            body=body,
            notification_type="briefing",
            data={"tasks": tasks, "events": events}
        )
    
    async def send_task_reminder(self, user_id: str, task: Dict):
        """Send task reminder notification"""
        await self.create_notification(
            user_id=user_id,
            title="Task Reminder",
            body=f"Reminder: {task['title']}",
            notification_type="reminder",
            data={"task_id": task["task_id"]}
        )