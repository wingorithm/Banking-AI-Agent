from datetime import datetime
from pydantic import BaseModel
from pydantic import BaseModel
from typing import Any, Optional

class GlobalResponse(BaseModel):
    http_status: int
    message: str
    content: Any

# TODO: Change to conversations Global Response
class GeneralResponse(BaseModel):
    message: str
    role: str
    client_uuid: str
    timestamp: Optional[datetime] = None
    action: str