import datetime
from uuid import UUID
from pydantic import Field

from src.model.schemas.base import BaseSchemaModel

class CustomerDTO(BaseSchemaModel):
    id: UUID
    cin: str
    name: str
    account_no: str
    balance: float

# Other Class 
# class CustomerDTO(BaseSchemaModel):
#     id: uuid