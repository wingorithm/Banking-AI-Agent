from pydantic import Field
from uuid import UUID
from typing import Optional, Dict

from src.model.schemas.base import BaseSchemaModel

class FunctionJobDTO(BaseSchemaModel):
    customer_id: UUID
    function_name: str
    param_object: str
    param_value: Optional[Dict] = Field(None, description="JSON parameter values for the function")
    status: str