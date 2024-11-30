import fastapi
from loguru import logger
from typing import Any, List

from src.repository.crud.Customer import CustomerCRUDRepository
from src.model.schemas.customer import CustomerDTO
from src.model.schemas.response.BalanceResponse import BalanceResponse
from src.util.LogMessageTemplate import LogMessageTemplate
from src.util.FunctionCallSpec import FunctionCallSpec as FCS

class BankService():
    def __init__(self, crud_repo: CustomerCRUDRepository):
        self.crud_repo = crud_repo

    async def get_data(self, customer_id: str, function_call_spesification: FCS) -> Any:
        logger.info(LogMessageTemplate.SERVICE_START.value.format(f="get_data", p=customer_id))
        try:
            if function_call_spesification.is_data:
                # Dynamically call the function based on function name
                function_name = function_call_spesification.function_name
                if not hasattr(self, function_name):
                    raise AttributeError(f"No such method '{function_name}' in BankService.")
                
                function_call = getattr(self, function_name)
                if callable(function_call):
                    logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(f="get_data", s=f"getting data from {function_name}", p=customer_id))
                    return await function_call(customer_id)
                else:
                    raise TypeError(f"Attribute '{function_name}' is not callable.")
        except Exception as e:
            logger.error(LogMessageTemplate.SERVICE_ERROR.value.format(f="get_data", p=customer_id, e=e))
            raise
    
    async def get_customers(self) -> List[CustomerDTO]:
        try:
            customers = await self.crud_repo.read_customers()
            logger.info(f"Successfully retrieved {len(customers)} customers.")
            
            return customers
        except Exception as e:
            logger.error(f"Error retrieving customers: {e}")
            raise

    async def get_balance(self, customer_id : str) -> BalanceResponse:
        try:
            customer = await self.crud_repo.read_customer_by_id(customer_id)
            logger.info(f"Successfully retrieved {customer.name} data.")
            
            return BalanceResponse(
                accountBalance=customer.balance,
                accountHolderName=customer.name,
                accountNumber=customer.account_no
            )
        except Exception as e:
            logger.error(f"Error retrieving customers: {e}")
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