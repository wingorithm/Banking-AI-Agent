import typing
import fastapi
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.orm import sessionmaker

from src.api.dependencies.session import get_async_session
from src.repository.crud.base import BaseCRUDRepository


def get_repository(
    repo_type: typing.Type[BaseCRUDRepository],
) -> typing.Callable[[SQLAlchemyAsyncSession], BaseCRUDRepository]:
    """
    Factory function to create repository dependencies.
    
    Args:
        repo_type: The repository class to instantiate
        
    Returns:
        A dependency function that creates a repository instance
    """
    def _get_repo(
        async_session: SQLAlchemyAsyncSession = fastapi.Depends(get_async_session),
    ) -> BaseCRUDRepository:
        return repo_type(async_session=async_session)

    return _get_repo