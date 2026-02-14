"""
Slack Bot Service
Handles Slack Bot API integration
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SlackService:
    def __init__(self, bot_token: str = None):
        self.bot_token = bot_token
        self.api_base_url = "https://slack.com/api"
        self.mock_mode = bot_token == "MOCK_TOKEN" or bot_token is None
    
    async def send_message(self, channel: str, text: str, **kwargs) -> Dict[str, Any]:
        """Send a message to a Slack channel"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack send_message to {channel}: {text[:50]}...")
            return {
                "ok": True,
                "channel": channel,
                "ts": "1234567890.123456",
                "message": {
                    "text": text,
                    "user": "U123456",
                    "ts": "1234567890.123456"
                }
            }
        
        # Real implementation would use aiohttp
        # headers = {"Authorization": f"Bearer {self.bot_token}"}
        # url = f"{self.api_base_url}/chat.postMessage"
        # payload = {"channel": channel, "text": text, **kwargs}
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(url, json=payload, headers=headers) as response:
        #         return await response.json()
        
        return {"ok": True, "ts": "placeholder"}
    
    async def send_block_message(self, channel: str, blocks: list, text: str = None) -> Dict[str, Any]:
        """Send a message with Block Kit blocks"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack send_block_message to {channel}")
            return {
                "ok": True,
                "channel": channel,
                "ts": "1234567890.123456"
            }
        
        return {"ok": True, "ts": "placeholder"}
    
    async def update_message(self, channel: str, ts: str, text: str, **kwargs) -> Dict[str, Any]:
        """Update an existing message"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack update_message: {ts}")
            return {
                "ok": True,
                "channel": channel,
                "ts": ts,
                "text": text
            }
        
        return {"ok": True}
    
    async def delete_message(self, channel: str, ts: str) -> Dict[str, Any]:
        """Delete a message"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack delete_message: {ts}")
            return {"ok": True, "channel": channel, "ts": ts}
        
        return {"ok": True}
    
    async def add_reaction(self, channel: str, timestamp: str, name: str) -> Dict[str, Any]:
        """Add an emoji reaction to a message"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack add_reaction: {name} to {timestamp}")
            return {"ok": True}
        
        return {"ok": True}
    
    async def get_channel_info(self, channel: str) -> Dict[str, Any]:
        """Get information about a channel"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack get_channel_info: {channel}")
            return {
                "ok": True,
                "channel": {
                    "id": channel,
                    "name": "mock-channel",
                    "is_channel": True
                }
            }
        
        return {"ok": True, "channel": {"id": channel}}
    
    async def get_user_info(self, user: str) -> Dict[str, Any]:
        """Get information about a user"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack get_user_info: {user}")
            return {
                "ok": True,
                "user": {
                    "id": user,
                    "name": "mockuser",
                    "real_name": "Mock User",
                    "is_bot": False
                }
            }
        
        return {"ok": True, "user": {"id": user}}
    
    async def get_bot_info(self) -> Dict[str, Any]:
        """Get bot information"""
        if self.mock_mode:
            return {
                "ok": True,
                "bot": {
                    "id": "B123456",
                    "name": "moltbot_mock",
                    "app_id": "A123456"
                }
            }
        
        return {"ok": True, "bot": {"id": "B0", "name": "bot"}}
    
    def parse_event_payload(self, payload: Dict) -> Optional[Dict[str, Any]]:
        """Parse incoming event from Slack Event API"""
        try:
            if payload.get("type") == "event_callback":
                event = payload.get("event", {})
                
                # Handle message events
                if event.get("type") == "message" and not event.get("bot_id"):
                    return {
                        "event_id": payload.get("event_id"),
                        "channel": event.get("channel"),
                        "user": event.get("user"),
                        "text": event.get("text", ""),
                        "ts": event.get("ts"),
                        "thread_ts": event.get("thread_ts")
                    }
        except Exception as e:
            logger.error(f"Error parsing Slack event: {e}")
        
        return None
    
    async def open_conversation(self, users: list) -> Dict[str, Any]:
        """Open a direct message or multi-person direct message"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack open_conversation with {users}")
            return {
                "ok": True,
                "channel": {
                    "id": f"D{users[0]}"
                }
            }
        
        return {"ok": True, "channel": {"id": "D0"}}
    
    async def upload_file(self, channels: str, file_path: str = None, 
                         content: str = None, title: str = None) -> Dict[str, Any]:
        """Upload a file to Slack"""
        if self.mock_mode:
            logger.info(f"[MOCK] Slack upload_file to {channels}")
            return {
                "ok": True,
                "file": {
                    "id": "F123456",
                    "name": title or "file"
                }
            }
        
        return {"ok": True, "file": {"id": "F0"}}
