import fastapi
import loguru

from src.api.dependencies.repository import get_repository
from src.repository.crud.Customer import CustomerCRUDRepository
from src.model.schemas.customer import CustomerDTO
import typing


class BankService():

    def __init__(
        self, 
        crud_repo: CustomerCRUDRepository = fastapi.Depends(get_repository(repo_type=CustomerCRUDRepository)),
        # Add other dependencies
    ):
        self.crud_repo = crud_repo


    async def get_customers(self) -> typing.List[CustomerDTO]:
        try:
            customers = await self.crud_repo.read_customers()
            loguru.logger.info(f"Successfully retrieved {len(customers)} customers.")
            
            return customers
        except Exception as e:
            loguru.logger.error(f"Error retrieving customers: {e}")
            raise

    # def fundTransfer(data : transferDetails):
    #     amount = Decimal(str(data.amount))
    #     sender = cd.find_customer_byAcc(data.debittedAccount)
    #     receiver = cd.find_customer_byAcc(data.credittedAccount)

    #     senderInitialBlance = sender.balance
    #     receiverInitialBlance = receiver.balance

    #     if sender is None or receiver is None:
    #         raise ValueError("Sender or receiver does not exist")

    #     if sender.balance < amount or amount < 1:
    #         raise ValueError("Insufficient balance")

    #     sender.set_balance(sender.get_balance() - amount)
    #     receiver.set_balance(receiver.get_balance() + amount)

    #     if(receiverInitialBlance != receiver.balance or senderInitialBlance != sender.balance ):
    #         cd.update_customer(sender, receiver)
        
    #     print("Fund transfer successful")
    
    # def get_account(client_uuid: str):
    #     account = cd.find_customer(client_uuid)
    #     if not account:
    #         raise ValueError("Customer not found")
    #     return sourceAccount(account.account, account.name, account.balance) 