import fastapi
from loguru import logger
from typing import List
from datetime import datetime

from src.repository.proxy.LLMProxy import LLMProxy 
from src.repository.crud.Document import DocumentsCRUDRepository
from src.util.FunctionCallSpec import FunctionCallSpec as FCS
from src.util.LogMessageTemplate import LogMessageTemplate
from src.util.LLMPromptTemplate import LLMPromptTemplate as PROMPT
from src.util.AgentResponseConstant import AgentResponseConstant
from src.model.schemas.response.GlobalResponse import AgentChatResponse
from src.model.schemas.Document import DocumentDTO
from src.model.schemas.request.LLMInferenceRequest import LLMInferenceRequest

"""
user this service as orchestrator to call other service based on intent
"""
class AgentService():
    def __init__(self, llm_proxy: LLMProxy, document_repo: DocumentsCRUDRepository):
        self.document_repo = document_repo
        self.llm_proxy = llm_proxy

    async def get_response(self, customer_id: str, user_message: str, function_name: str) -> AgentChatResponse[FCS]:
        logger.info(LogMessageTemplate.SERVICE_START.value.format(f="get_response", p=customer_id))
        try:
            logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(f="get_response", s="executing action based on intent...", p=customer_id))
            function_call_spesification, message = await self.__execute_action_by_intent(customer_id, user_message, function_name)

            return AgentChatResponse(
                message=message,
                role="agent",
                timestamp=datetime.utcnow(),
                action=function_call_spesification.function_name,
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
            # CHECK if need job queue
            if(function_call_spesification.is_job):
                await self.__register_function_call_job()
            
            # CHECK if need RAG Retrieval
            if(function_call_spesification.is_rag):
                rag_result = await self.document_repo.search_related_documents(message=user_message)
            
            # CHECK if need LLM Inference
            if(function_call_spesification.is_invoke):
                message = await self.__invoke_LLM_response(customer_id, user_message, rag_result)
            else:
                message = await self.__get_agent_constant_message(function_call_spesification)

            return function_call_spesification, message
        except Exception as e:
            logger.error(LogMessageTemplate.SERVICE_ERROR.value.format(f="execute_action_by_intent", p=customer_id, e=e))
            raise
        finally:
            logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(f="execute_action_by_intent", p=customer_id))

    async def __invoke_LLM_response(self, customer_id: str, user_message: str, context: List[DocumentDTO]) -> str:
        appended_context = []
        for hit in context:
            appended_context.append(hit.original_chunk)
        context_string = "\n".join(appended_context)

        logger.info(LogMessageTemplate.SERVICE_PROGRESS.value.format(f="__invoke_LLM_response", s=f"getting response for", p=customer_id))
        payload = LLMInferenceRequest(
            prompt = PROMPT.OLLAMA_PROMPT.value.format(context=context_string, question=user_message)
        )
        return await self.llm_proxy.generate_response(payload=payload, customer_id=customer_id)

    async def __get_agent_constant_message(self, function_call_spesification: FCS):
        response_mapping = {
            "GET_BALANCE": AgentResponseConstant.GET_BALANCE,
            # Add more costant mappings as needed
        }
        return response_mapping.get(function_call_spesification.name, "No message defined for this spec.")
    
    #TODO SOON PHASE 2
    async def __register_function_call_job(self) -> None:
        logger.info(LogMessageTemplate.SERVICE_COMPLETE.value.format(f="__register_action_to_job", p="#soon"))