import datetime
import uuid
import pydantic

from src.model.schemas.base import BaseSchemaModel

class CustomerDTO(BaseSchemaModel):
    id: uuid
    username: str
    name: str
    accountNo: str
    balance: float
    created_at: datetime.datetime
    updated_at: datetime.datetime | None