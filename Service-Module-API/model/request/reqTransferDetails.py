from pydantic import BaseModel
from decimal import Decimal

class reqTransferDetails(BaseModel):
    debittedAccount : str 
    creditedcreditedName : str
    credittedAccount : str
    amount : Decimal