import fastapi
from loguru import logger

from src.util.LogMessageTemplate import LogMessageTemplate

class IntentClassificationService:
    def __init__(self):
        pass  # Placeholder for future needs

    async def classify_intent(self, customer_id: str, user_message: str) -> str:
        logger.info(LogMessageTemplate.SERVICE_START.value.format(
            f="classify_intent", p=customer_id))
        try:
            logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(
                f="classify_intent", s="calculating intent", p=customer_id))
            
            # TODO @Adriel to integrate with LLM function calling
            return "get_balance"

        except Exception as e:
            logger.error(LogMessageTemplate.SERVICE_ERROR.value.format(
                f="classify_intent", p=customer_id, e=e))
            raise
        finally:
            logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(
                f="classify_intent", p=customer_id))
