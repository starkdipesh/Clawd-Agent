"""
Unified Messaging Service
Handles message routing and processing across all platforms
"""
from datetime import datetime
from typing import Optional, Dict, Any
import uuid


class MessagingService:
    def __init__(self, db):
        self.db = db
        self.bots_collection = db.bot_configurations
        self.messages_collection = db.message_syncs
    
    async def get_bot_by_id(self, bot_id: str) -> Optional[Dict]:
        """Get bot configuration by ID"""
        return await self.bots_collection.find_one({"bot_id": bot_id})
    
    async def get_bot_by_platform_and_user(self, platform: str, user_id: str) -> Optional[Dict]:
        """Get bot configuration by platform and user"""
        return await self.bots_collection.find_one({
            "platform": platform,
            "user_id": user_id,
            "enabled": True
        })
    
    async def get_all_bots(self, user_id: str) -> list:
        """Get all bot configurations for a user"""
        cursor = self.bots_collection.find({"user_id": user_id})
        return await cursor.to_list(length=100)
    
    async def create_bot_config(self, user_id: str, platform: str, bot_name: str, 
                                bot_token: str, settings: Dict = None) -> Dict:
        """Create a new bot configuration"""
        bot_config = {
            "bot_id": str(uuid.uuid4()),
            "user_id": user_id,
            "platform": platform,
            "bot_name": bot_name,
            "bot_token": bot_token,
            "webhook_url": None,
            "settings": settings or {},
            "enabled": True,
            "status": "active",
            "last_message_at": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await self.bots_collection.insert_one(bot_config)
        return bot_config
    
    async def update_bot_config(self, bot_id: str, updates: Dict) -> bool:
        """Update bot configuration"""
        updates["updated_at"] = datetime.utcnow()
        result = await self.bots_collection.update_one(
            {"bot_id": bot_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    async def delete_bot_config(self, bot_id: str) -> bool:
        """Delete bot configuration"""
        result = await self.bots_collection.delete_one({"bot_id": bot_id})
        return result.deleted_count > 0
    
    async def toggle_bot(self, bot_id: str, enabled: bool) -> bool:
        """Enable or disable a bot"""
        return await self.update_bot_config(bot_id, {"enabled": enabled})
    
    async def save_message_sync(self, bot_id: str, platform: str, platform_message_id: str,
                                user_id: str, direction: str, content: str,
                                sender_name: str = None, sender_id: str = None,
                                metadata: Dict = None) -> Dict:
        """Save a synced message"""
        message_sync = {
            "sync_id": str(uuid.uuid4()),
            "bot_id": bot_id,
            "platform": platform,
            "platform_message_id": platform_message_id,
            "user_id": user_id,
            "direction": direction,
            "content": content,
            "sender_name": sender_name,
            "sender_id": sender_id,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow(),
            "ai_response": None,
            "processed": False
        }
        
        await self.messages_collection.insert_one(message_sync)
        
        # Update bot's last message timestamp
        await self.bots_collection.update_one(
            {"bot_id": bot_id},
            {"$set": {"last_message_at": datetime.utcnow()}}
        )
        
        return message_sync
    
    async def update_message_sync(self, sync_id: str, updates: Dict) -> bool:
        """Update a synced message"""
        result = await self.messages_collection.update_one(
            {"sync_id": sync_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    async def get_message_history(self, bot_id: str, limit: int = 50) -> list:
        """Get message history for a bot"""
        cursor = self.messages_collection.find(
            {"bot_id": bot_id}
        ).sort("timestamp", -1).limit(limit)
        
        return await cursor.to_list(length=limit)
    
    async def get_user_message_history(self, user_id: str, platform: str = None, 
                                       limit: int = 100) -> list:
        """Get all message history for a user, optionally filtered by platform"""
        query = {"user_id": user_id}
        if platform:
            query["platform"] = platform
        
        cursor = self.messages_collection.find(query).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def mark_message_processed(self, sync_id: str, ai_response: str = None) -> bool:
        """Mark a message as processed with optional AI response"""
        updates = {"processed": True}
        if ai_response:
            updates["ai_response"] = ai_response
        
        return await self.update_message_sync(sync_id, updates)
    
    async def get_bot_stats(self, bot_id: str) -> Dict[str, Any]:
        """Get statistics for a bot"""
        total_messages = await self.messages_collection.count_documents({"bot_id": bot_id})
        incoming = await self.messages_collection.count_documents({
            "bot_id": bot_id,
            "direction": "incoming"
        })
        outgoing = await self.messages_collection.count_documents({
            "bot_id": bot_id,
            "direction": "outgoing"
        })
        
        # Get last message
        last_message = await self.messages_collection.find_one(
            {"bot_id": bot_id},
            sort=[("timestamp", -1)]
        )
        
        return {
            "total_messages": total_messages,
            "incoming_messages": incoming,
            "outgoing_messages": outgoing,
            "last_message_at": last_message["timestamp"] if last_message else None
        }
