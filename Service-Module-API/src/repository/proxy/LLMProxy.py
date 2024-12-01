import httpx
from loguru import logger

from src.util.exceptions.ExternalServiceException import ExternalServiceException
from src.model.schemas.request import LLMInferenceRequest
from src.util.LogMessageTemplate import LogMessageTemplate
from src.repository.crud.base import BaseProxy


class LLMProxy(BaseProxy):

    async def generate_response(self, payload: LLMInferenceRequest, customer_id: str) -> str:
        try:
            logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(f="generate_response", s=f"trying to hot LLM", p=customer_id))
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(
                    connect=10.0,
                    read=120.0,
                    write=10.0,
                    pool=10.0
                )
            ) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload.dict()
                )
                response.raise_for_status()
                return response.json()["response"]
        except httpx.HTTPError as e:
            raise ExternalServiceException(
                message="Error calling LLM endpoint",
                service_name="LLMProxy",
                status_code=500,
                details={str(e)}
            )
