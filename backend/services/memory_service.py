from typing import List, Dict, Optional, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

class MemoryService:
    def __init__(self, db):
        self.db = db
        self.memories = db.memories
        self.conversations = db.conversations
        self.messages = db.messages
    
    async def store_memory(self, user_id: str, key: str, value: Any, context: str = "", importance: int = 5):
        """Store a memory for the user"""
        memory = {
            "user_id": user_id,
            "key": key,
            "value": value,
            "context": context,
            "importance": importance,
            "created_at": datetime.utcnow(),
            "last_accessed": datetime.utcnow()
        }
        result = await self.memories.insert_one(memory)
        return str(result.inserted_id)
    
    async def get_memories(self, user_id: str, key: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Retrieve memories for a user"""
        query = {"user_id": user_id}
        if key:
            query["key"] = key
        
        cursor = self.memories.find(query).sort("importance", -1).limit(limit)
        memories = await cursor.to_list(length=limit)
        
        # Remove MongoDB _id field
        for memory in memories:
            memory.pop("_id", None)
        
        return memories
    
    async def get_conversation_context(self, conversation_id: str, limit: int = 10) -> List[Dict]:
        """Get recent messages from a conversation"""
        cursor = self.messages.find(
            {"conversation_id": conversation_id}
        ).sort("timestamp", -1).limit(limit)
        
        messages = await cursor.to_list(length=limit)
        return list(reversed(messages))  # Oldest first
    
    async def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user context including memories and preferences"""
        memories = await self.get_memories(user_id, limit=20)
        user = await self.db.users.find_one({"user_id": user_id})
        
        if user:
            user.pop("_id", None)  # Remove MongoDB _id
        else:
            user = {"name": "User", "preferences": {}}
        
        return {
            "name": user.get("name", "User"),
            "preferences": user.get("preferences", {}),
            "memories": memories
        }
    
    async def update_memory(self, user_id: str, key: str, value: Any):
        """Update an existing memory"""
        await self.memories.update_one(
            {"user_id": user_id, "key": key},
            {
                "$set": {
                    "value": value,
                    "last_accessed": datetime.utcnow()
                }
            },
            upsert=True
        )
    
    async def extract_and_store_insights(self, user_id: str, conversation_id: str):
        """Analyze conversation and extract important information to store as memories"""
        messages = await self.get_conversation_context(conversation_id, limit=20)
        
        # Simple keyword-based extraction (can be enhanced with AI)
        keywords = ["remember", "my name is", "i like", "i don't like", "i prefer", "important"]
        
        for msg in messages:
            if msg["role"] == "user":
                content_lower = msg["content"].lower()
                for keyword in keywords:
                    if keyword in content_lower:
                        await self.store_memory(
                            user_id=user_id,
                            key=f"conversation_insight_{msg['message_id']}",
                            value=msg["content"],
                            context=f"From conversation {conversation_id}",
                            importance=7
                        )