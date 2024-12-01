from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from src.repository.milvus_manager import MilvusManager

"""
@BaseCRUDRepository -> act like Interface for all crud repository implementations   
"""
class BaseCRUDRepository:
    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.async_session = async_session

class VectorCRUDRepository:
    def __init__(self, milvus_manager: MilvusManager):
        self.manager = milvus_manager
        self.client = None  # Lazy Initialization connection
        self.collection_name = "bank_documents"

class BaseProxy:
    def __init__(self, base_url: str):
        self.base_url = base_url