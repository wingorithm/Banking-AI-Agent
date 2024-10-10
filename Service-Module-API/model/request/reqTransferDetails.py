from pydantic import BaseModel
from decimal import Decimal

class reqTransferDetails(BaseModel):
    beneficiaryAccount : str 
    sourceAccount : str
    sourceAccountName : str
    amount : Decimal