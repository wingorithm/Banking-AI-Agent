import fastapi
from loguru import logger

from src.api.dependencies.repository import get_repository
from src.repository.crud.Customer import CustomerCRUDRepository
from src.util.LogMessageTemplate import LogMessageTemplate
from src.util.AgentResponseConstant import AgentResponseConstant
from src.model.schemas.response.GlobalResponse import AgentChatResponse
from src.model.schemas.response.BalanceResponse import BalanceResponse
from src.service.BankService import BankService
from datetime import datetime
import typing

"""
user this service as orchestrator to call other service based on intent
"""


class AgentService():

    def __init__(
        self,
        crud_repo: CustomerCRUDRepository = fastapi.Depends(
            get_repository(repo_type=CustomerCRUDRepository)),
        # Add other dependencies
    ):
        self.crud_repo = crud_repo

    # TODO : create flow for -> Intent classification -> LLM RAG -> getting userdata -> return
    async def get_response(self, customer_id: str, user_message: str, function_name: str) -> AgentChatResponse[BalanceResponse]:
        logger.info(LogMessageTemplate.SERVICE_START.value.format(
            f="get_response", p=customer_id))
        try:
            logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(
                f="get_response", s="executing action based on intent...", p=customer_id))

            data, message = await self.__execute_action_by_intent(
                customer_id, function_name)

            return AgentChatResponse(
                message=message,
                role="agent",
                timestamp=datetime.utcnow(),
                action=function_name,
                data=data
            )

        except Exception as e:
            logger.error(LogMessageTemplate.SERVICE_ERROR.value.format(
                f="get_response", p=customer_id, e=e))
            raise
        finally:
            logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(
                f="get_response", p=customer_id))

    """
    __execute_action_by_intent will return tuple with format:
        -> data(additional data) , message(llm response)
    """
    async def __execute_action_by_intent(self, customer_id: str, function_name: str) -> tuple:
        try:
            match function_name:
                case "question_answering":
                    logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(
                        f="execute_action_by_intent", s="getting result from question_answering", p=customer_id))
                    return "dummy data", "call RAG", "" #TODO : soon

                case "get_balance":
                    logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(
                        f="execute_action_by_intent", s="getting result from get_balance", p=customer_id))
                    balance  = await BankService.get_balance(customer_id=customer_id)
                    return balance, AgentResponseConstant.BALANCE

                case "fund_transfer":
                    logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(
                        f="execute_action_by_intent", s="getting result from fund_transfer", p=customer_id))
                    return "dummy data", "add job queue + return detail transfer" #TODO : soon

                case "transaction_history":
                    logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(
                        f="execute_action_by_intent", s="getting result from transaction_history", p=customer_id))
                    return "dummy data", "add job queue + return transaction history" #TODO : soon

                case _:
                    raise ValueError(
                        f"Unsupported function_name: {function_name}")

        except Exception as e:
            logger.error(LogMessageTemplate.SERVICE_ERROR.value.format(
                f="execute_action_by_intent", p=customer_id, e=e))
            raise
        finally:
            logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(
                f="execute_action_by_intent", p=customer_id))
