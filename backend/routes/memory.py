from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
from pydantic import BaseModel

from services.memory_service import MemoryService

router = APIRouter(prefix="/api/memory", tags=["memory"])

def get_db():
    from server import db
    return db

class MemoryCreate(BaseModel):
    user_id: str
    key: str
    value: Any
    context: str = ""
    importance: int = 5

@router.post("/store")
async def store_memory(memory: MemoryCreate):
    """Store a memory"""
    try:
        db = get_db()
        memory_service = MemoryService(db)
        
        memory_id = await memory_service.store_memory(
            user_id=memory.user_id,
            key=memory.key,
            value=memory.value,
            context=memory.context,
            importance=memory.importance
        )
        
        return {"success": True, "memory_id": memory_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{user_id}")
async def get_memories(
    user_id: str,
    key: Optional[str] = None,
    limit: int = 10
):
    """Get user memories"""
    try:
        db = get_db()
        memory_service = MemoryService(db)
        
        memories = await memory_service.get_memories(user_id, key, limit)
        
        for memory in memories:
            memory.pop("_id", None)
        
        return {"memories": memories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/context/{user_id}")
async def get_user_context(user_id: str):
    """Get comprehensive user context"""
    try:
        db = get_db()
        memory_service = MemoryService(db)
        
        context = await memory_service.get_user_context(user_id)
        
        # Clean MongoDB _id fields
        for memory in context.get("memories", []):
            memory.pop("_id", None)
        
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))