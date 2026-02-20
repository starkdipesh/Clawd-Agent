import os
from emergentintegrations.llm.chat import LlmChat, UserMessage
from typing import List, Dict, Optional
import uuid
import re
from .skill_service import SkillService

class AIService:
    def __init__(self, db=None):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        self.skill_service = SkillService(db) if db else None
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """Generate AI response using Emergent LLM key"""
        try:
            # Get last user message
            last_message = messages[-1]['content'] if messages else "Hello"
            
            # Check if this is a skill request
            skill_response = await self._check_skill_request(last_message)
            if skill_response:
                return skill_response
            
            # Create a unique session ID
            session_id = str(uuid.uuid4())
            
            # Initialize chat with emergentintegrations
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_prompt or "You are a helpful AI assistant named Moltbot."
            ).with_model("openai", "gpt-4o")
            
            # Create user message
            user_message = UserMessage(text=last_message)
            
            # Send message and get response
            response = await chat.send_message(user_message)
            
            return response
        except Exception as e:
            print(f"AI Service Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"I apologize, but I encountered an error: {str(e)}"
    
    async def _check_skill_request(self, message: str) -> Optional[str]:
        """Check if message is a skill request and execute it"""
        if not self.skill_service:
            return None
            
        message_lower = message.lower().strip()
        
        # Weather skill patterns
        weather_patterns = [
            r'weather\s+in\s+([a-zA-Z\s]+)',
            r'what(?:\'?s|s)?\s+the\s+weather\s+like\s+in\s+([a-zA-Z\s]+)',
            r'give\s+me\s+weather\s+(?:update|for)\s+([a-zA-Z\s]+)',
            r'temperature\s+in\s+([a-zA-Z\s]+)',
            r'how\s+(?:hot|cold|warm|cold)\s+is\s+it\s+in\s+([a-zA-Z\s]+)'
        ]
        
        for pattern in weather_patterns:
            match = re.search(pattern, message_lower)
            if match:
                location = match.group(1).strip()
                result = await self.skill_service.execute_skill("weather", {"location": location})
                if result["success"]:
                    return result["result"]
                else:
                    return f"❌ Weather skill error: {result['error']}"
        
        # Web search skill patterns
        web_search_patterns = [
            r'search\s+(?:for|about)?\s+(.+)',
            r'find\s+(?:information|about)?\s+(.+)',
            r'look\s+up\s+(.+)',
            r'google\s+(.+)'
        ]
        
        for pattern in web_search_patterns:
            match = re.search(pattern, message_lower)
            if match:
                query = match.group(1).strip()
                result = await self.skill_service.execute_skill("web_search", {"query": query})
                if result["success"]:
                    return result["result"]
                else:
                    return f"❌ Web search skill error: {result['error']}"
        
        # Calendar skill patterns
        calendar_patterns = [
            r'calendar\s+(.+)',
            r'add\s+(?:event|meeting)\s+(.+)',
            r'what(?:\'?s|s)?\s+(?:on\s+)?(?:my\s+)?schedule',
            r'show\s+(?:me\s+)?(?:my\s+)?(?:events|appointments)'
        ]
        
        for pattern in calendar_patterns:
            match = re.search(pattern, message_lower)
            if match:
                if 'add' in message_lower or 'meeting' in message_lower or 'event' in message_lower:
                    result = await self.skill_service.execute_skill("calendar", {"action": "add", "event": match.group(1).strip()})
                    if result["success"]:
                        return result["result"]
                    else:
                        return f"❌ Calendar skill error: {result['error']}"
                else:
                    result = await self.skill_service.execute_skill("calendar", {"action": "list"})
                    if result["success"]:
                        return result["result"]
                    else:
                        return f"❌ Calendar skill error: {result['error']}"
        
        # Email skill patterns
        email_patterns = [
            r'email\s+(.+)',
            r'check\s+(?:my\s+)?(?:inbox|emails?)',
            r'send\s+(?:email|mail)\s+(?:to\s+)?(.+)',
            r'compose\s+(?:email|mail)'
        ]
        
        for pattern in email_patterns:
            match = re.search(pattern, message_lower)
            if match:
                if 'send' in message_lower or 'compose' in message_lower:
                    result = await self.skill_service.execute_skill("email", {"action": "send"})
                    if result["success"]:
                        return result["result"]
                    else:
                        return f"❌ Email skill error: {result['error']}"
                else:
                    result = await self.skill_service.execute_skill("email", {"action": "inbox"})
                    if result["success"]:
                        return result["result"]
                    else:
                        return f"❌ Email skill error: {result['error']}"
        
        # Notes skill patterns
        notes_patterns = [
            r'notes?\s+(.+)',
            r'add\s+note\s+(.+)',
            r'take\s+a\s+note\s+(.+)',
            r'show\s+(?:me\s+)?(?:my\s+)?notes?'
        ]
        
        for pattern in notes_patterns:
            match = re.search(pattern, message_lower)
            if match:
                if 'add' in message_lower or 'take' in message_lower:
                    result = await self.skill_service.execute_skill("notes", {"action": "add", "note": match.group(1).strip()})
                    if result["success"]:
                        return result["result"]
                    else:
                        return f"❌ Notes skill error: {result['error']}"
                elif 'search' in message_lower:
                    result = await self.skill_service.execute_skill("notes", {"action": "search", "query": match.group(1).strip()})
                    if result["success"]:
                        return result["result"]
                    else:
                        return f"❌ Notes skill error: {result['error']}"
                else:
                    result = await self.skill_service.execute_skill("notes", {"action": "list"})
                    if result["success"]:
                        return result["result"]
                    else:
                        return f"❌ Notes skill error: {result['error']}"
        
        return None
    
    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ):
        """Generate streaming AI response"""
        try:
            # Get last user message
            last_message = messages[-1]['content'] if messages else "Hello"
            
            # Check if this is a skill request
            skill_response = await self._check_skill_request(last_message)
            if skill_response:
                yield skill_response
                return
            
            session_id = str(uuid.uuid4())
            
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_prompt or "You are a helpful AI assistant named Moltbot."
            ).with_model("openai", "gpt-4o")
            
            last_message = messages[-1]['content'] if messages else "Hello"
            user_message = UserMessage(text=last_message)
            
            response = await chat.send_message(user_message)
            yield response
        except Exception as e:
            yield f"Error: {str(e)}"

ai_service = AIService()