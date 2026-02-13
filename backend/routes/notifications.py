from fastapi import APIRouter, HTTPException
from services.notification_service import NotificationService

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

def get_db():
    from server import db
    return db

@router.get("/list/{user_id}")
async def get_notifications(user_id: str, unread_only: bool = False, limit: int = 50):
    """Get user notifications"""
    try:
        db = get_db()
        notification_service = NotificationService(db)
        
        notifications = await notification_service.get_notifications(user_id, unread_only, limit)
        
        for notif in notifications:
            notif["_id"] = str(notif["_id"])
        
        return {"notifications": notifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/read/{notification_id}")
async def mark_notification_read(notification_id: str):
    """Mark notification as read"""
    try:
        db = get_db()
        notification_service = NotificationService(db)
        
        success = await notification_service.mark_as_read(notification_id)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))