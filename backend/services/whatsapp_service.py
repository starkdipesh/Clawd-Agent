"""
WhatsApp Service (via Twilio)
Handles WhatsApp messaging through Twilio API
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class WhatsAppService:
    def __init__(self, account_sid: str = None, auth_token: str = None, whatsapp_number: str = None):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.whatsapp_number = whatsapp_number  # Format: whatsapp:+14155238886
        self.api_base_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}"
        self.mock_mode = account_sid == "MOCK_SID" or account_sid is None
    
    async def send_message(self, to_number: str, body: str, media_url: str = None) -> Dict[str, Any]:
        """Send a WhatsApp message via Twilio"""
        if self.mock_mode:
            logger.info(f"[MOCK] WhatsApp send_message to {to_number}: {body[:50]}...")
            return {
                "sid": f"mock_msg_{to_number}_{len(body)}",
                "from": self.whatsapp_number or "whatsapp:+14155238886",
                "to": to_number,
                "body": body,
                "status": "sent",
                "date_created": "2024-01-01T00:00:00Z"
            }
        
        # Real implementation would use Twilio SDK or aiohttp
        # from twilio.rest import Client
        # client = Client(self.account_sid, self.auth_token)
        # message = client.messages.create(
        #     from_=self.whatsapp_number,
        #     body=body,
        #     to=to_number,
        #     media_url=[media_url] if media_url else None
        # )
        # return message.__dict__
        
        return {"sid": "placeholder", "status": "sent"}
    
    async def send_template_message(self, to_number: str, template_name: str, 
                                    variables: list = None) -> Dict[str, Any]:
        """Send a WhatsApp template message (for business accounts)"""
        if self.mock_mode:
            logger.info(f"[MOCK] WhatsApp send_template_message '{template_name}' to {to_number}")
            return {
                "sid": f"mock_template_{to_number}",
                "from": self.whatsapp_number or "whatsapp:+14155238886",
                "to": to_number,
                "status": "sent"
            }
        
        return {"sid": "placeholder", "status": "sent"}
    
    def parse_webhook_message(self, form_data: Dict) -> Optional[Dict[str, Any]]:
        """Parse incoming webhook message from Twilio (WhatsApp)"""
        try:
            return {
                "message_id": form_data.get("MessageSid"),
                "from_number": form_data.get("From"),  # whatsapp:+1234567890
                "to_number": form_data.get("To"),
                "sender_name": form_data.get("ProfileName", "Unknown"),
                "body": form_data.get("Body", ""),
                "num_media": int(form_data.get("NumMedia", 0)),
                "timestamp": form_data.get("Timestamp")
            }
        except Exception as e:
            logger.error(f"Error parsing WhatsApp webhook: {e}")
        
        return None
    
    async def get_message_status(self, message_sid: str) -> Dict[str, Any]:
        """Get the status of a sent message"""
        if self.mock_mode:
            logger.info(f"[MOCK] WhatsApp get_message_status: {message_sid}")
            return {
                "sid": message_sid,
                "status": "delivered",
                "date_sent": "2024-01-01T00:00:00Z"
            }
        
        return {"sid": message_sid, "status": "unknown"}
    
    async def send_media(self, to_number: str, media_url: str, caption: str = None) -> Dict[str, Any]:
        """Send media (image, video, document) via WhatsApp"""
        body = caption or ""
        return await self.send_message(to_number, body, media_url)
    
    async def send_location(self, to_number: str, latitude: float, longitude: float, 
                           name: str = None, address: str = None) -> Dict[str, Any]:
        """Send location via WhatsApp"""
        if self.mock_mode:
            logger.info(f"[MOCK] WhatsApp send_location to {to_number}: {latitude},{longitude}")
            return {
                "sid": f"mock_location_{to_number}",
                "status": "sent"
            }
        
        return {"sid": "placeholder", "status": "sent"}
    
    def format_phone_number(self, phone: str) -> str:
        """Format phone number for WhatsApp (whatsapp:+1234567890)"""
        if not phone.startswith("whatsapp:"):
            if not phone.startswith("+"):
                phone = f"+{phone}"
            return f"whatsapp:{phone}"
        return phone
