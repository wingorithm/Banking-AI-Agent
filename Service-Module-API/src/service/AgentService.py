import fastapi
from loguru import logger

from src.repository.crud.Customer import CustomerCRUDRepository
from src.repository.crud.Document import DocumentsCRUDRepository
from src.util.FunctionCallSpec import FunctionCallSpec as FCS
from src.util.LogMessageTemplate import LogMessageTemplate
from src.util.AgentResponseConstant import AgentResponseConstant
from src.model.schemas.response.GlobalResponse import AgentChatResponse
from datetime import datetime

"""
user this service as orchestrator to call other service based on intent
"""
class AgentService():
    def __init__(self, crud_repo: CustomerCRUDRepository, document_repo: DocumentsCRUDRepository):
        self.crud_repo = crud_repo
        self.document_repo = document_repo

    async def get_response(self, customer_id: str, user_message: str, function_name: str) -> AgentChatResponse[FCS]:
        logger.info(LogMessageTemplate.SERVICE_START.value.format(f="get_response", p=customer_id))
        try:
            logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(f="get_response", s="executing action based on intent...", p=customer_id))
            function_call_spesification, message = await self.__execute_action_by_intent(customer_id, user_message, function_name)

            return AgentChatResponse(
                message=message,
                role="agent",
                timestamp=datetime.utcnow(),
                action=function_call_spesification,
                data=None
            )

        except Exception as e:
            logger.error(LogMessageTemplate.SERVICE_ERROR.value.format(
                f="get_response", p=customer_id, e=e))
            raise
        finally:
            logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(
                f="get_response", p=customer_id))

    """
    this function will do action (create job, validate request or return message) based on function name
    @Return 1.FunctionCallSpec, 2.message(llm response)
    """
    async def __execute_action_by_intent(self, customer_id: str, user_message: str, function_name: str) -> tuple:
        try:

            logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(f="execute_action_by_intent", s="getting function call spec...", p=customer_id))
            function_call_spesification = FCS.get_by_alias(function_name)

            logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(f="execute_action_by_intent", s=f"executing {function_call_spesification.name} spec...", p=customer_id))
            if(function_call_spesification.is_job):
                await self.__register_function_call_job()
            
            if(function_call_spesification.is_rag):
                rag_result = await self.document_repo.search_related_documents(message=user_message)
            
            if(function_call_spesification.is_invoke):
                message = await self.__invoke_LLM_response(customer_id, function_call_spesification, rag_result)
            else:
                return await self.__get_agent_constant_message(function_call_spesification)

            return function_call_spesification, message
        except Exception as e:
            logger.error(LogMessageTemplate.SERVICE_ERROR.value.format(f="execute_action_by_intent", p=customer_id, e=e))
            raise
        finally:
            logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(f="execute_action_by_intent", p=customer_id))

    async def __invoke_LLM_response(self, customer_id: str, function_call_spesification: FCS, context: any) -> str:
        logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(f="__invoke_LLM_response", s=f"getting response for {function_call_spesification.name}", p=customer_id))
        return "this is LLM Response"
        
    #TODO SOON PHASE 2
    async def __register_function_call_job(self) -> None:
        logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(f="__register_action_to_job", p="#soon"))

    async def __get_agent_constant_message(self, function_call_spesification: FCS):
        response_mapping = {
            "GET_BALANCE": AgentResponseConstant.GET_BALANCE,
            # Add more costant mappings as needed
        }
        return response_mapping.get(function_call_spesification.name, "No message defined for this spec.")