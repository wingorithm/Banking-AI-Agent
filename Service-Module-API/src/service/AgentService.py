import fastapi
from loguru import logger

from src.api.dependencies.repository import get_repository
from src.repository.crud.Customer import CustomerCRUDRepository
from src.util.LogMessageTemplate import LogMessageTemplate
from src.model.schemas.response.GlobalResponse import AgentChatResponse
from src.service.RAGService import RAGService
from datetime import datetime
import typing


class AgentService():

    def __init__(
        self,
        crud_repo: CustomerCRUDRepository = fastapi.Depends(
            get_repository(repo_type=CustomerCRUDRepository)),
        # Add other dependencies
    ):
        self.crud_repo = crud_repo
        self.rag_service = RAGService()

    # TODO : create flow for -> Intent classification -> LLM RAG -> getting userdata -> return
    async def get_response(self, customer_id: str, user_message: str) -> typing.List[AgentChatResponse]:
        logger.info(LogMessageTemplate.SERVICE_START.value.format(
            f="get_response", p=customer_id))
        try:
            logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(
                f="get_response", s="getting customer data", p=customer_id))
            customer = await self.crud_repo.read_customer_by_id(customer_id)
        
            message = await self.rag_service.rag_chain(user_message)

            return AgentChatResponse(
                message=f"{message}",
                role="agent",
                client_uuid=customer_id,
                timestamp=datetime.utcnow(),
                action="chat"
            )

        except Exception as e:
            logger.error(LogMessageTemplate.SERVICE_ERROR.value.format(
                f="get_response", p=customer_id, e=e))
            raise
        finally:
            logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(
                f="get_response", p=customer_id))


# class RetrievalService:

#     async def getRespond(user_message : generalResponse):
#         print("start preprocessing")
#         user_message.setTimestamp(datetime.now())

#         last_word = user_message.message.split()[-1]
#         if last_word == "transfer":
#             user_message.setRole("action")
#             user_message.setMessage("transfer")
#             return user_message
#         elif last_word == "balance":
#             user_message.setRole("action")
#             user_message.setMessage("balance")
#             return user_message
#         else:
#             # TODO : GANTI LLM Adriel
#             nluPreprocessing.NamedEntityRecognitionModel(user_message.message)
#             nluPreprocessing.intentClassificationModel(user_message.message)
#             user_message.setMessage(nluService.LLM(user_message.message))
#             print(user_message.message)
#             user_message.setRole("bot")
#             # TODO : Bikin null clientuuid
#             return user_message
