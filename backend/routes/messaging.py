"""
Messaging Routes
Handles bot configuration and message routing for all platforms
"""
from fastapi import APIRouter, HTTPException, Request, Body
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from models.schemas import BotConfigRequest, WebhookMessage
from services.messaging_service import MessagingService
from services.telegram_service import TelegramService
from services.discord_service import DiscordService
from services.whatsapp_service import WhatsAppService
from services.slack_service import SlackService
from services.ai_service import AIService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/messaging", tags=["messaging"])

# Global database reference (will be set from server.py)
db = None

def set_db(database):
    global db
    db = database


@router.post("/config/create")
async def create_bot_configuration(config: BotConfigRequest):
    """Create a new bot configuration"""
    try:
        messaging_service = MessagingService(db)
        
        # Check if bot already exists for this platform
        existing = await messaging_service.get_bot_by_platform_and_user(
            config.platform, config.user_id
        )
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Bot already configured for {config.platform}"
            )
        
        # Create bot configuration
        bot_config = await messaging_service.create_bot_config(
            user_id=config.user_id,
            platform=config.platform,
            bot_name=config.bot_name,
            bot_token=config.bot_token,
            settings=config.settings
        )
        
        return {
            "success": True,
            "bot_id": bot_config["bot_id"],
            "message": f"{config.platform} bot configured successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating bot config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config/list/{user_id}")
async def get_user_bots(user_id: str):
    """Get all bot configurations for a user"""
    try:
        messaging_service = MessagingService(db)
        bots = await messaging_service.get_all_bots(user_id)
        
        # Add stats for each bot
        for bot in bots:
            stats = await messaging_service.get_bot_stats(bot["bot_id"])
            bot["stats"] = stats
        
        return {"bots": bots, "count": len(bots)}
    
    except Exception as e:
        logger.error(f"Error getting user bots: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config/get/{bot_id}")
async def get_bot_configuration(bot_id: str):
    """Get a specific bot configuration"""
    try:
        messaging_service = MessagingService(db)
        bot = await messaging_service.get_bot_by_id(bot_id)
        
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        # Add stats
        stats = await messaging_service.get_bot_stats(bot_id)
        bot["stats"] = stats
        
        return bot
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting bot config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/config/update/{bot_id}")
async def update_bot_configuration(bot_id: str, updates: Dict[str, Any] = Body(...)):
    """Update bot configuration"""
    try:
        messaging_service = MessagingService(db)
        
        # Remove fields that shouldn't be updated directly
        updates.pop("bot_id", None)
        updates.pop("user_id", None)
        updates.pop("created_at", None)
        
        success = await messaging_service.update_bot_config(bot_id, updates)
        
        if not success:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        return {"success": True, "message": "Bot configuration updated"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating bot config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/config/delete/{bot_id}")
async def delete_bot_configuration(bot_id: str):
    """Delete a bot configuration"""
    try:
        messaging_service = MessagingService(db)
        success = await messaging_service.delete_bot_config(bot_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        return {"success": True, "message": "Bot deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting bot config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/config/toggle/{bot_id}")
async def toggle_bot(bot_id: str, enabled: bool = Body(..., embed=True)):
    """Enable or disable a bot"""
    try:
        messaging_service = MessagingService(db)
        success = await messaging_service.toggle_bot(bot_id, enabled)
        
        if not success:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        status = "enabled" if enabled else "disabled"
        return {"success": True, "message": f"Bot {status}"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error toggling bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send/{bot_id}")
async def send_message(
    bot_id: str,
    recipient: str = Body(...),
    message: str = Body(...),
    metadata: Dict[str, Any] = Body(default={})
):
    """Send a message through a bot"""
    try:
        messaging_service = MessagingService(db)
        bot = await messaging_service.get_bot_by_id(bot_id)
        
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        if not bot["enabled"]:
            raise HTTPException(status_code=400, detail="Bot is disabled")
        
        # Send message based on platform
        platform = bot["platform"]
        result = None
        
        if platform == "telegram":
            service = TelegramService(bot["bot_token"])
            result = await service.send_message(recipient, message)
        
        elif platform == "discord":
            service = DiscordService(bot["bot_token"])
            result = await service.send_message(recipient, message)
        
        elif platform == "whatsapp":
            settings = bot.get("settings", {})
            service = WhatsAppService(
                account_sid=settings.get("account_sid"),
                auth_token=settings.get("auth_token"),
                whatsapp_number=settings.get("whatsapp_number")
            )
            result = await service.send_message(recipient, message)
        
        elif platform == "slack":
            service = SlackService(bot["bot_token"])
            result = await service.send_message(recipient, message)
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
        
        # Save message sync
        await messaging_service.save_message_sync(
            bot_id=bot_id,
            platform=platform,
            platform_message_id=str(result.get("id") or result.get("message_id", "unknown")),
            user_id=bot["user_id"],
            direction="outgoing",
            content=message,
            metadata={"recipient": recipient, "result": result}
        )
        
        return {
            "success": True,
            "message": "Message sent successfully",
            "result": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/messages/{bot_id}")
async def get_message_history(bot_id: str, limit: int = 50):
    """Get message history for a bot"""
    try:
        messaging_service = MessagingService(db)
        messages = await messaging_service.get_message_history(bot_id, limit)
        
        return {"messages": messages, "count": len(messages)}
    
    except Exception as e:
        logger.error(f"Error getting message history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook/telegram/{bot_id}")
async def telegram_webhook(bot_id: str, request: Request):
    """Webhook endpoint for Telegram"""
    try:
        messaging_service = MessagingService(db)
        bot = await messaging_service.get_bot_by_id(bot_id)
        
        if not bot or not bot["enabled"]:
            raise HTTPException(status_code=404, detail="Bot not found or disabled")
        
        update = await request.json()
        logger.info(f"Telegram webhook received for bot {bot_id}")
        
        # Parse update
        service = TelegramService(bot["bot_token"])
        parsed = service.parse_webhook_update(update)
        
        if parsed:
            # Save incoming message
            sync = await messaging_service.save_message_sync(
                bot_id=bot_id,
                platform="telegram",
                platform_message_id=parsed["message_id"],
                user_id=bot["user_id"],
                direction="incoming",
                content=parsed["text"],
                sender_name=parsed["sender_name"],
                sender_id=parsed["sender_id"],
                metadata={"chat_id": parsed["chat_id"]}
            )
            
            # Process with AI (if enabled)
            if bot.get("settings", {}).get("ai_enabled", True):
                ai_service = AIService(db)
                ai_response = await ai_service.generate_response(
                    bot["user_id"],
                    parsed["text"]
                )
                
                # Send AI response back
                await service.send_message(parsed["chat_id"], ai_response)
                
                # Update sync with AI response
                await messaging_service.mark_message_processed(
                    sync["sync_id"],
                    ai_response
                )
        
        return {"ok": True}
    
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")
        return {"ok": False, "error": str(e)}


@router.post("/webhook/discord/{bot_id}")
async def discord_webhook(bot_id: str, request: Request):
    """Webhook endpoint for Discord"""
    try:
        messaging_service = MessagingService(db)
        bot = await messaging_service.get_bot_by_id(bot_id)
        
        if not bot or not bot["enabled"]:
            raise HTTPException(status_code=404, detail="Bot not found or disabled")
        
        payload = await request.json()
        logger.info(f"Discord webhook received for bot {bot_id}")
        
        # Handle Discord verification
        if payload.get("type") == 1:  # PING
            return {"type": 1}
        
        # Parse message
        service = DiscordService(bot["bot_token"])
        parsed = service.parse_webhook_payload(payload)
        
        if parsed:
            # Similar processing as Telegram...
            await messaging_service.save_message_sync(
                bot_id=bot_id,
                platform="discord",
                platform_message_id=parsed["message_id"],
                user_id=bot["user_id"],
                direction="incoming",
                content=parsed["content"],
                sender_name=parsed["sender_name"],
                sender_id=parsed["sender_id"],
                metadata={"channel_id": parsed["channel_id"]}
            )
        
        return {"ok": True}
    
    except Exception as e:
        logger.error(f"Error processing Discord webhook: {e}")
        return {"ok": False, "error": str(e)}


@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """Webhook endpoint for WhatsApp (Twilio)"""
    try:
        form_data = await request.form()
        logger.info("WhatsApp webhook received")
        
        # Parse Twilio form data
        service = WhatsAppService()
        parsed = service.parse_webhook_message(dict(form_data))
        
        if parsed:
            # Find bot by phone number
            messaging_service = MessagingService(db)
            # For now, just log it
            logger.info(f"WhatsApp message: {parsed}")
        
        # Twilio expects empty 200 response
        return {}
    
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {e}")
        return {}


@router.post("/webhook/slack")
async def slack_webhook(request: Request):
    """Webhook endpoint for Slack Events API"""
    try:
        payload = await request.json()
        logger.info("Slack webhook received")
        
        # Handle Slack URL verification
        if payload.get("type") == "url_verification":
            return {"challenge": payload.get("challenge")}
        
        # Parse event
        service = SlackService()
        parsed = service.parse_event_payload(payload)
        
        if parsed:
            logger.info(f"Slack message: {parsed}")
        
        return {"ok": True}
    
    except Exception as e:
        logger.error(f"Error processing Slack webhook: {e}")
        return {"ok": False}
