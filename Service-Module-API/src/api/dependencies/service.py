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
def get_bank_service() -> BankService:
    crud_repo_factory = get_repository(repo_type=CustomerCRUDRepository)
    crud_repo = crud_repo_factory()
    return BankService(crud_repo=crud_repo)

def get_agent_service() -> AgentService:
    bank_service=get_bank_service()
    document_repo=get_documents_repository()
    crud_repo=get_repository(repo_type=CustomerCRUDRepository)
    return AgentService(crud_repo=crud_repo, document_repo=document_repo, bank_service=bank_service)

def get_intent_classification_service():
    return IntentClassificationService()