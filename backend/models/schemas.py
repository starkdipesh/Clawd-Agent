from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    user_id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Conversation(BaseModel):
    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str = "New Conversation"
    messages: List[str] = Field(default_factory=list)  # message_ids
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Memory(BaseModel):
    memory_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    key: str  # memory key/category
    value: Any  # memory content
    context: str = ""  # additional context
    importance: int = 5  # 1-10
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)

class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high
    status: str = "pending"  # pending, completed, cancelled
    recurring: bool = False
    recurrence_pattern: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class Skill(BaseModel):
    skill_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category: str
    enabled: bool = True
    config: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"

class ChatRequest(BaseModel):
    user_id: str
    conversation_id: Optional[str] = None
    message: str
    use_voice: bool = False

class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)