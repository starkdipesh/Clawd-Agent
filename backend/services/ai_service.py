import os
from emergentintegrations.llm.chat import LlmChat, UserMessage
from typing import List, Dict, Optional
import uuid

class AIService:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """Generate AI response using Emergent LLM key"""
        try:
            # Create a unique session ID
            session_id = str(uuid.uuid4())
            
            # Initialize chat with emergentintegrations
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_prompt or "You are a helpful AI assistant named Moltbot."
            ).with_model("openai", "gpt-4o")
            
            # Get the last user message
            last_message = messages[-1]['content'] if messages else "Hello"
            
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
    
    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ):
        """Generate streaming AI response"""
        try:
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