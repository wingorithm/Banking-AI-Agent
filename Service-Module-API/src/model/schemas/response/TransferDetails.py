from pydantic import BaseModel

class TransferDetails(BaseModel):
    beneficiaryAccount: str
    sourceName: str
    sourceAccount: str
    amount: float