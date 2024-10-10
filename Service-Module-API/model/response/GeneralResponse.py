from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GeneralResponse(BaseModel):
    message: str
    role: str
    client_uuid: str
    timestamp: Optional[datetime] = None
    action: str