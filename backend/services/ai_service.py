import os
from openai import OpenAI
from typing import List, Dict, Optional

class AIService:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.emergentmethods.ai/v1"
        )
        self.model = "gpt-4o-mini"  # Fast and free with Emergent key
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """Generate AI response using Emergent LLM key"""
        try:
            formatted_messages = []
            
            if system_prompt:
                formatted_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            formatted_messages.extend(messages)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI Service Error: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ):
        """Generate streaming AI response"""
        try:
            formatted_messages = []
            
            if system_prompt:
                formatted_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            formatted_messages.extend(messages)
            
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                stream=True,
                max_tokens=1000
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error: {str(e)}"

ai_service = AIService()