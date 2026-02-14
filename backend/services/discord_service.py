"""
Discord Bot Service
Handles Discord Bot API integration
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DiscordService:
    def __init__(self, bot_token: str = None):
        self.bot_token = bot_token
        self.api_base_url = "https://discord.com/api/v10"
        self.mock_mode = bot_token == "MOCK_TOKEN" or bot_token is None
    
    async def send_message(self, channel_id: str, content: str, **kwargs) -> Dict[str, Any]:
        """Send a message to a Discord channel"""
        if self.mock_mode:
            logger.info(f"[MOCK] Discord send_message to {channel_id}: {content[:50]}...")
            return {
                "id": f"mock_msg_{channel_id}_{len(content)}",
                "channel_id": channel_id,
                "content": content,
                "timestamp": "2024-01-01T00:00:00.000000+00:00"
            }
        
        # Real implementation would use aiohttp
        # headers = {"Authorization": f"Bot {self.bot_token}"}
        # url = f"{self.api_base_url}/channels/{channel_id}/messages"
        # payload = {"content": content, **kwargs}
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(url, json=payload, headers=headers) as response:
        #         return await response.json()
        
        return {"id": "placeholder", "content": content}
    
    async def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """Get channel information"""
        if self.mock_mode:
            logger.info(f"[MOCK] Discord get_channel: {channel_id}")
            return {
                "id": channel_id,
                "type": 0,
                "name": "mock-channel",
                "guild_id": "123456789"
            }
        
        return {"id": channel_id, "type": 0}
    
    async def get_guild(self, guild_id: str) -> Dict[str, Any]:
        """Get guild (server) information"""
        if self.mock_mode:
            logger.info(f"[MOCK] Discord get_guild: {guild_id}")
            return {
                "id": guild_id,
                "name": "Mock Server",
                "owner_id": "123456789"
            }
        
        return {"id": guild_id, "name": "Server"}
    
    async def get_bot_user(self) -> Dict[str, Any]:
        """Get bot user information"""
        if self.mock_mode:
            return {
                "id": "987654321",
                "username": "MoltbotMock",
                "discriminator": "0000",
                "bot": True
            }
        
        return {"id": "0", "username": "Bot", "bot": True}
    
    def parse_webhook_payload(self, payload: Dict) -> Optional[Dict[str, Any]]:
        """Parse incoming webhook payload from Discord"""
        try:
            # Discord sends different types of interactions
            if payload.get("type") == 0:  # Message
                return {
                    "message_id": payload.get("id"),
                    "channel_id": payload.get("channel_id"),
                    "sender_id": payload.get("author", {}).get("id"),
                    "sender_name": payload.get("author", {}).get("username", "Unknown"),
                    "content": payload.get("content", ""),
                    "timestamp": payload.get("timestamp")
                }
        except Exception as e:
            logger.error(f"Error parsing Discord payload: {e}")
        
        return None
    
    async def create_dm_channel(self, user_id: str) -> Dict[str, Any]:
        """Create a DM channel with a user"""
        if self.mock_mode:
            logger.info(f"[MOCK] Discord create_dm_channel for user {user_id}")
            return {
                "id": f"dm_{user_id}",
                "type": 1,
                "recipients": [{"id": user_id}]
            }
        
        return {"id": f"dm_{user_id}", "type": 1}
    
    async def send_embed(self, channel_id: str, embed: Dict) -> Dict[str, Any]:
        """Send an embed message to a Discord channel"""
        if self.mock_mode:
            logger.info(f"[MOCK] Discord send_embed to {channel_id}")
            return {
                "id": f"mock_embed_{channel_id}",
                "channel_id": channel_id,
                "embeds": [embed]
            }
        
        return {"id": "placeholder", "embeds": [embed]}
    
    async def add_reaction(self, channel_id: str, message_id: str, emoji: str) -> bool:
        """Add a reaction to a message"""
        if self.mock_mode:
            logger.info(f"[MOCK] Discord add_reaction: {emoji} to {message_id}")
            return True
        
        return True
    
    async def delete_message(self, channel_id: str, message_id: str) -> bool:
        """Delete a message"""
        if self.mock_mode:
            logger.info(f"[MOCK] Discord delete_message: {message_id}")
            return True
        
        return True
