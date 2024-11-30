import typing
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from src.api.dependencies.session import get_async_session
from src.repository.crud.base import BaseCRUDRepository
from src.repository.milvus_manager import MilvusManager
from src.repository.crud.Document import DocumentsCRUDRepository
from src.repository.crud.Customer import CustomerCRUDRepository
from src.service.AgentService import AgentService
from src.service.BankService import BankService
from src.service.IntentClassificationService import IntentClassificationService

"""
Factory function to create repository dependencies.

Args:
    repo_type: The repository class to instantiate
    
Returns:
    A dependency function that creates a repository instance
"""
def get_repository(
    repo_type: typing.Type[BaseCRUDRepository],
) -> typing.Callable[[SQLAlchemyAsyncSession], BaseCRUDRepository]:
    def _get_repo(
        async_session: SQLAlchemyAsyncSession = Depends(get_async_session),
    ) -> BaseCRUDRepository:
        return repo_type(async_session=async_session)

    return _get_repo

def get_milvus_manager(app: FastAPI) -> MilvusManager:
    if not hasattr(app.state, "milvus"):
        raise Exception("Milvus connection not initialized.")
    return app.state.milvus

def get_documents_repository(
    milvus_manager: MilvusManager = Depends(get_milvus_manager)
) -> DocumentsCRUDRepository:
    return DocumentsCRUDRepository(milvus_manager=milvus_manager)