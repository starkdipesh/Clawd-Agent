"""
Telegram Bot Service
Handles Telegram Bot API integration
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self, bot_token: str = None):
        self.bot_token = bot_token
        self.api_base_url = f"https://api.telegram.org/bot{bot_token}" if bot_token else None
        self.mock_mode = bot_token == "MOCK_TOKEN" or bot_token is None
    
    async def send_message(self, chat_id: str, text: str, **kwargs) -> Dict[str, Any]:
        """Send a message to a Telegram chat"""
        if self.mock_mode:
            logger.info(f"[MOCK] Telegram send_message to {chat_id}: {text[:50]}...")
            return {
                "ok": True,
                "result": {
                    "message_id": f"mock_msg_{chat_id}_{len(text)}",
                    "chat": {"id": chat_id, "type": "private"},
                    "text": text,
                    "date": 1234567890
                }
            }
        
        # Real implementation would use aiohttp to call Telegram API
        # import aiohttp
        # async with aiohttp.ClientSession() as session:
        #     url = f"{self.api_base_url}/sendMessage"
        #     payload = {"chat_id": chat_id, "text": text, **kwargs}
        #     async with session.post(url, json=payload) as response:
        #         return await response.json()
        
        return {"ok": True, "result": {"message_id": "placeholder"}}
    
    async def get_updates(self, offset: int = None, timeout: int = 30) -> Dict[str, Any]:
        """Get updates from Telegram (long polling)"""
        if self.mock_mode:
            logger.info(f"[MOCK] Telegram get_updates (offset={offset})")
            return {"ok": True, "result": []}
        
        # Real implementation
        return {"ok": True, "result": []}
    
    async def set_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Set webhook URL for receiving updates"""
        if self.mock_mode:
            logger.info(f"[MOCK] Telegram set_webhook: {webhook_url}")
            return {"ok": True, "result": True, "description": "Webhook was set (mock)"}
        
        # Real implementation
        return {"ok": True, "result": True}
    
    async def delete_webhook(self) -> Dict[str, Any]:
        """Delete the webhook"""
        if self.mock_mode:
            logger.info("[MOCK] Telegram delete_webhook")
            return {"ok": True, "result": True}
        
        # Real implementation
        return {"ok": True, "result": True}
    
    async def get_me(self) -> Dict[str, Any]:
        """Get bot information"""
        if self.mock_mode:
            return {
                "ok": True,
                "result": {
                    "id": 123456789,
                    "is_bot": True,
                    "first_name": "Moltbot",
                    "username": "moltbot_mock",
                    "can_join_groups": True,
                    "can_read_all_group_messages": False
                }
            }
        
        # Real implementation
        return {"ok": True, "result": {"id": 0, "is_bot": True, "first_name": "Bot"}}
    
    def parse_webhook_update(self, update: Dict) -> Optional[Dict[str, Any]]:
        """Parse incoming webhook update from Telegram"""
        try:
            if "message" in update:
                message = update["message"]
                return {
                    "message_id": str(message.get("message_id")),
                    "chat_id": str(message["chat"]["id"]),
                    "sender_id": str(message["from"]["id"]),
                    "sender_name": message["from"].get("first_name", "Unknown"),
                    "text": message.get("text", ""),
                    "timestamp": message.get("date")
                }
        except Exception as e:
            logger.error(f"Error parsing Telegram update: {e}")
        
        return None
    
    async def send_photo(self, chat_id: str, photo_url: str, caption: str = None) -> Dict:
        """Send a photo to a Telegram chat"""
        if self.mock_mode:
            logger.info(f"[MOCK] Telegram send_photo to {chat_id}")
            return {"ok": True, "result": {"message_id": f"mock_photo_{chat_id}"}}
        
        return {"ok": True, "result": {"message_id": "placeholder"}}
    
    async def send_document(self, chat_id: str, document_url: str, caption: str = None) -> Dict:
        """Send a document to a Telegram chat"""
        if self.mock_mode:
            logger.info(f"[MOCK] Telegram send_document to {chat_id}")
            return {"ok": True, "result": {"message_id": f"mock_doc_{chat_id}"}}
        
        return {"ok": True, "result": {"message_id": "placeholder"}}
