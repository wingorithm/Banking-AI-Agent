from loguru import logger

import sqlalchemy
import uuid

from src.model.db.FunctionJob import FunctionJob
from src.model.schemas.FunctionJob import FunctionJobDTO
from src.repository.crud.base import BaseCRUDRepository
from src.util.exceptions.DatabaseExceptions import EntityDoesNotExist
from src.util.LogMessageTemplate import LogMessageTemplate

class FunctionJobCRUDRepository(BaseCRUDRepository):
    async def read_job_by_id(self, id: str) -> FunctionJobDTO:
        logger.info(LogMessageTemplate.REPO_START.value.format(q="read_job_by_id", p=id))
        
        stmt = sqlalchemy.select(FunctionJob).where(FunctionJob.customer_id == uuid.UUID(id))
        result = await self.async_session.execute(statement=stmt)
        job = result.scalar()

        if not job:
            raise EntityDoesNotExist(f"FunctionJob with id `{id}` does not exist!")

        logger.info(LogMessageTemplate.REPO_COMPLETE.value.format(q="read_job_by_id", res=job))
        return FunctionJobDTO.from_orm(job)