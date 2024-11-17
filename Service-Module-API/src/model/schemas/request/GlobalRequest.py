from pydantic import BaseModel

class AgentChatRequest(BaseModel):
    message: str
    role: str