from src.api.dependencies.repository import *
from src.repository.crud.Customer import CustomerCRUDRepository
from src.repository.proxy.LLMProxy import LLMProxy 
from src.service.AgentService import AgentService
from src.service.BankService import BankService
from src.service.IntentClassificationService import IntentClassificationService

"""
Factory function to create service dependencies.

-> encapsulate the creation logic for service objects.
-> provides a central place to handle the initialization of complex objects.
"""
def get_bank_service(
    crud_repo: CustomerCRUDRepository = Depends(get_repository(repo_type=CustomerCRUDRepository))
) -> BankService:
    return BankService(crud_repo=crud_repo)


def get_agent_service() -> AgentService:
    document_repo=get_documents_repository()
    llm_proxy=get_proxy()
    return AgentService(llm_proxy=llm_proxy, document_repo=document_repo)

def get_intent_classification_service():
    return IntentClassificationService()