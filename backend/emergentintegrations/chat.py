# Main emergentintegrations module
import asyncio
from typing import Optional

class UserMessage:
    def __init__(self, text: str):
        self.text = text

class LlmChat:
    def __init__(self, api_key: str, session_id: str, system_message: str):
        self.api_key = api_key
        self.session_id = session_id
        self.system_message = system_message
        self.model = None
    
    def with_model(self, provider: str, model: str):
        self.model = f"{provider}:{model}"
        return self
    
    async def send_message(self, user_message: UserMessage) -> str:
        # Mock response for development
        await asyncio.sleep(0.1)  # Simulate API delay
        
        responses = [
            "Hello! I'm Moltbot, your AI assistant. How can I help you today?",
            "That's an interesting question! Let me think about that...",
            "I understand what you're saying. Here's my response...",
            "As Moltbot, I'm here to assist you with various tasks.",
            "Thanks for your message! I'm processing your request..."
        ]
        
        # Simple keyword-based responses
        text = user_message.text.lower()
        if "hello" in text or "hi" in text:
            return "Hello! I'm Moltbot, your AI assistant. How can I help you today?"
        elif "help" in text:
            return "I can help you with tasks, chat, weather, web search, and more. What do you need help with?"
        elif "task" in text:
            return "I can help you manage tasks! You can create, update, and track your to-do items."
        elif "weather" in text:
            return "I can check the weather for you. Just let me know your location!"
        elif "bye" in text or "goodbye" in text:
            return "Goodbye! Feel free to chat with me anytime."
        else:
            import random
            return random.choice(responses)
