from pydantic import BaseModel

class SourceAccount(BaseModel):
    accountNumber: str
    accountHolderName: str
    balance: float

    def to_string(self) -> str:
        return self.json()