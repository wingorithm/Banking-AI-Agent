from typing import Type, Callable
from fastapi import Depends
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from src.api.dependencies.session import get_async_session
from src.repository.crud.base import BaseCRUDRepository, BaseProxy
from src.repository.milvus_manager import MilvusManager
from src.repository.crud.Document import DocumentsCRUDRepository
from src.config.manager import settings
from src.repository.proxy.LLMProxy import LLMProxy 

"""
Factory function to create repository dependencies.

Args:
    repo_type: The repository class to instantiate
    
Returns:
    A dependency function that creates a repository instance
"""
def get_repository(
    repo_type: Type[BaseCRUDRepository],
) -> Callable[[SQLAlchemyAsyncSession], BaseCRUDRepository]:
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

"""
Dependency injection for creating proxy instances dynamically.
# TODO : Create generic if more proxy handle
"""
def get_proxy() -> LLMProxy:
    return LLMProxy(base_url=settings.LLM_HOST)