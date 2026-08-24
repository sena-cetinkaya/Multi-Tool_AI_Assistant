from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ToolCallRecord(BaseModel):
    tool_name: str
    tool_input: Any
    tool_output: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: list[ToolCallRecord] = Field(default_factory=list)

class AgentResponse(BaseModel):
    content: str
    tool_calls: list[ToolCallRecord] = Field(default_factory=list)
    success: bool = True
    error_message: Optional[str] = None
