import typing
import loguru
from loguru import logger

import sqlalchemy
import uuid

from src.model.db.customer import Customer
from src.model.schemas.customer import CustomerDTO
from src.repository.crud.base import BaseCRUDRepository
from src.util.exceptions.DatabaseExceptions import EntityDoesNotExist
from src.util.LogMessageTemplate import LogMessageTemplate

class CustomerCRUDRepository(BaseCRUDRepository):

    async def read_customers(self) -> typing.Sequence[CustomerDTO]:
        loguru.logger.info(f"PROGRESS accessing data...")
        stmt = sqlalchemy.select(Customer)
        query = await self.async_session.execute(statement=stmt)
        customers = query.scalars().all()
        loguru.logger.info(f"COMPLETE accessing data: {len(customers)}")

        return [CustomerDTO.from_orm(customer) for customer in customers]

    async def read_customer_by_id(self, id: str) -> typing.Sequence[CustomerDTO]:
        logger.info(LogMessageTemplate.REPO_START.value.format(q="read_customer_by_id", p=id))
        customer_id = uuid.UUID(id)
        stmt = sqlalchemy.select(Customer).where(Customer.id == customer_id)
        
        result = await self.async_session.execute(statement=stmt)
        customer = result.scalar()
        
        if not customer:
            raise EntityDoesNotExist(f"Customer with id `{id}` does not exist!")
        
        logger.info(LogMessageTemplate.REPO_COMPLETE.value.format(q="read_customer_by_id", res=customer))
        return CustomerDTO.from_orm(customer)

    # async def update_account_by_id(self, id: int, account_update: AccountInUpdate) -> Account:
    #     new_account_data = account_update.dict()

    #     select_stmt = sqlalchemy.select(Account).where(Account.id == id)
    #     query = await self.async_session.execute(statement=select_stmt)
    #     update_account = query.scalar()

    #     if not update_account:
    #         raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")  # type: ignore

    #     update_stmt = sqlalchemy.update(table=Account).where(Account.id == update_account.id).values(updated_at=sqlalchemy_functions.now())  # type: ignore

    #     if new_account_data["username"]:
    #         update_stmt = update_stmt.values(username=new_account_data["username"])

    #     if new_account_data["email"]:
    #         update_stmt = update_stmt.values(username=new_account_data["email"])

    #     if new_account_data["password"]:
    #         update_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)  # type: ignore
    #         update_account.set_hashed_password(hashed_password=pwd_generator.generate_hashed_password(hash_salt=update_account.hash_salt, new_password=new_account_data["password"]))  # type: ignore

    #     await self.async_session.execute(statement=update_stmt)
    #     await self.async_session.commit()
    #     await self.async_session.refresh(instance=update_account)

    #     return update_account  # type: ignore

    # async def delete_account_by_id(self, id: int) -> str:
    #     select_stmt = sqlalchemy.select(Account).where(Account.id == id)
    #     query = await self.async_session.execute(statement=select_stmt)
    #     delete_account = query.scalar()

    #     if not delete_account:
    #         raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")  # type: ignore

    #     stmt = sqlalchemy.delete(table=Account).where(Account.id == delete_account.id)

    #     await self.async_session.execute(statement=stmt)
    #     await self.async_session.commit()

    #     return f"Account with id '{id}' is successfully deleted!"