from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/users", tags=["users"])

def get_db():
    from server import db
    return db

class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    preferences: Dict[str, Any] = {}

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

@router.post("/create")
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        db = get_db()
        
        user_data = {
            "user_id": str(uuid.uuid4()),
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "preferences": user.preferences,
            "created_at": datetime.utcnow()
        }
        
        await db.users.insert_one(user_data)
        
        return {
            "success": True,
            "user_id": user_data["user_id"],
            "name": user_data["name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{user_id}")
async def get_user(user_id: str):
    """Get user information"""
    try:
        db = get_db()
        
        user = await db.users.find_one({"user_id": user_id})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.pop("_id", None)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{user_id}")
async def update_user(user_id: str, update: UserUpdate):
    """Update user information"""
    try:
        db = get_db()
        
        updates = {k: v for k, v in update.dict().items() if v is not None}
        
        if not updates:
            return {"success": False, "message": "No updates provided"}
        
        result = await db.users.update_one(
            {"user_id": user_id},
            {"$set": updates}
        )
        
        return {"success": result.modified_count > 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_users():
    """List all users"""
    try:
        db = get_db()
        
        cursor = db.users.find({}).sort("created_at", -1)
        users = await cursor.to_list(length=100)
        
        for user in users:
            user.pop("_id", None)
        
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))