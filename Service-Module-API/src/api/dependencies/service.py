from src.api.dependencies.repository import *
from src.repository.crud.Customer import CustomerCRUDRepository
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
    crud_repo=get_repository(repo_type=CustomerCRUDRepository)
    return AgentService(crud_repo=crud_repo, document_repo=document_repo)

def get_intent_classification_service():
    return IntentClassificationService()