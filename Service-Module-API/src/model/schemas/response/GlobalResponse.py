from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional, Generic, TypeVar

T = TypeVar('T')

class GlobalResponse(BaseModel):
    http_status: int
    message: str
    content: Any

class AgentChatResponse(BaseModel, Generic[T]):
    message: str
    role: str
    timestamp: Optional[datetime] = None
    action: str
    data: Optional[T] = None