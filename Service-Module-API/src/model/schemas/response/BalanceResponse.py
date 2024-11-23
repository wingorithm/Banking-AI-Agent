from datetime import datetime
from pydantic import BaseModel
from typing import Any
from decimal import Decimal

class BalanceResponse(BaseModel):
    accountNumber: int
    accountHolderName: str
    accountBalance: Decimal