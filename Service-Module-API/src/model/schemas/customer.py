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

    @property
    def get_name(self) -> str:
        return self.name

    @get_name.setter
    def set_name(self, value: str) -> None: 
        self.name = value

    @property
    def get_account_no(self) -> str:
        return self.account_no

    @get_account_no.setter
    def set_account_no(self, value: str) -> None:
        self.account_no = value

    @property
    def get_balance(self) -> float:
        return self.balance

    @get_balance.setter
    def set_balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.balance = value

# Other Class 
# class CustomerDTO(BaseSchemaModel):
#     id: uuid