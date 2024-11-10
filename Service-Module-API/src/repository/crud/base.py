from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

"""
@BaseCRUDRepository -> act like Interface for all crud repository implementations   
"""
class BaseCRUDRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.async_session = async_session