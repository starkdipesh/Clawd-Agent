from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List, Dict
from datetime import datetime
import uuid
import json

from models.schemas import ChatRequest, ChatResponse, Message
from services.ai_service import ai_service
from services.memory_service import MemoryService

router = APIRouter(prefix="/api/chat", tags=["chat"])

def get_db():
    from server import db
    return db

@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message and get AI response"""
    try:
        db = get_db()
        memory_service = MemoryService(db)
        
        # Get or create conversation
        conversation_id = request.conversation_id
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            await db.conversations.insert_one({
                "conversation_id": conversation_id,
                "user_id": request.user_id,
                "title": request.message[:50],
                "messages": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
        
        # Store user message
        user_message_id = str(uuid.uuid4())
        user_message = {
            "message_id": user_message_id,
            "conversation_id": conversation_id,
            "user_id": request.user_id,
            "role": "user",
            "content": request.message,
            "timestamp": datetime.utcnow(),
            "metadata": {}
        }
        await db.messages.insert_one(user_message)
        
        # Get conversation context
        context_messages = await memory_service.get_conversation_context(conversation_id, limit=10)
        
        # Get user context and memories
        user_context = await memory_service.get_user_context(request.user_id)
        
        # Build system prompt with user context
        system_prompt = f"""You are a helpful AI assistant named Moltbot. You are proactive, intelligent, and capable of helping with various tasks.
        
User's name: {user_context['name']}
User preferences: {json.dumps(user_context['preferences'])}

Relevant memories:
{chr(10).join([f"- {m.get('value', '')}" for m in user_context['memories'][:5]])}

Be conversational, helpful, and remember the context from previous messages."""
        
        # Format messages for AI
        formatted_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in context_messages
        ]
        formatted_messages.append({"role": "user", "content": request.message})
        
        # Generate AI response
        ai_response = await ai_service.generate_response(
            messages=formatted_messages,
            system_prompt=system_prompt
        )
        
        # Store assistant message
        assistant_message_id = str(uuid.uuid4())
        assistant_message = {
            "message_id": assistant_message_id,
            "conversation_id": conversation_id,
            "user_id": request.user_id,
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.utcnow(),
            "metadata": {}
        }
        await db.messages.insert_one(assistant_message)
        
        # Update conversation
        await db.conversations.update_one(
            {"conversation_id": conversation_id},
            {
                "$push": {"messages": {"$each": [user_message_id, assistant_message_id]}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Extract insights for memory (async, don't wait)
        asyncio.create_task(memory_service.extract_and_store_insights(request.user_id, conversation_id))
        
        return ChatResponse(
            conversation_id=conversation_id,
            message_id=assistant_message_id,
            response=ai_response,
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{user_id}")
async def get_conversations(user_id: str):
    """Get all conversations for a user"""
    try:
        db = get_db()
        cursor = db.conversations.find({"user_id": user_id}).sort("updated_at", -1)
        conversations = await cursor.to_list(length=100)
        
        # Remove MongoDB _id field
        for conv in conversations:
            conv.pop("_id", None)
        
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messages/{conversation_id}")
async def get_messages(conversation_id: str, limit: int = 50):
    """Get messages from a conversation"""
    try:
        db = get_db()
        cursor = db.messages.find({"conversation_id": conversation_id}).sort("timestamp", 1).limit(limit)
        messages = await cursor.to_list(length=limit)
        
        # Remove MongoDB _id field
        for msg in messages:
            msg.pop("_id", None)
        
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation and its messages"""
    try:
        db = get_db()
        await db.messages.delete_many({"conversation_id": conversation_id})
        await db.conversations.delete_one({"conversation_id": conversation_id})
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import asyncio