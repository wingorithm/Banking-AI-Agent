import typing
import loguru

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.model.db.customer import Customer
from src.model.schemas.customer import CustomerDTO
from src.repository.crud.base import BaseCRUDRepository

class CustomerCRUDRepository(BaseCRUDRepository):
    # async def create_account(self, account_create: AccountInCreate) -> Account:
    #     new_account = Account(username=account_create.username, email=account_create.email, is_logged_in=True)

    #     new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
    #     new_account.set_hashed_password(
    #         hashed_password=pwd_generator.generate_hashed_password(
    #             hash_salt=new_account.hash_salt, new_password=account_create.password
    #         )
    #     )

    #     self.async_session.add(instance=new_account)
    #     await self.async_session.commit()
    #     await self.async_session.refresh(instance=new_account)

    #     return new_account

    async def read_customers(self) -> typing.Sequence[CustomerDTO]:
        loguru.logger.info(f"PROGRESS accessing data...")
        stmt = sqlalchemy.select(Customer)
        query = await self.async_session.execute(statement=stmt)
        customers = query.scalars().all()
        loguru.logger.info(f"COMPLETE accessing data: {len(customers)}")

        return [CustomerDTO.from_orm(customer) for customer in customers]

    # async def read_account_by_id(self, id: int) -> Customer:
    #     stmt = sqlalchemy.select(Customer).where(Account.id == id)
    #     query = await self.async_session.execute(statement=stmt)

    #     if not query:
    #         raise EntityDoesNotExist("Account with id `{id}` does not exist!")

    #     return query.scalar()  # type: ignore

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