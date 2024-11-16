import fastapi
import loguru

from src.model.schemas.customer import CustomerDTO
from src.model.schemas.response.GlobalResponse import GlobalResponse
from src.repository.crud.Customer import CustomerCRUDRepository
from src.service.BankService import BankService
# from src.util.exceptions.database import EntityDoesNotExist
# from src.util.exceptions.http.exc_404 import (
#     http_404_exc_email_not_found_request,
#     http_404_exc_id_not_found_request,
#     http_404_exc_username_not_found_request,
# )

router = fastapi.APIRouter(prefix="/customer", tags=["customer"])

@router.get(
    path="",
    name="customers:read-customers",
    response_model=GlobalResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_customers(bank_service: BankService = fastapi.Depends()) -> list[CustomerDTO]:
    loguru.logger.info(f"REQUESTING /customer endpoint")
    response = await bank_service.get_customers()
    loguru.logger.info(f"COMPLETE /customer endpoint")
    
    return GlobalResponse(
        http_status=200,
        message="Successfully retrieved customers",
        content=response
        )

# @router.get(
#     path="/{id}",
#     name="accountss:read-account-by-id",
#     response_model=AccountInResponse,
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def get_account(
#     id: int,
#     account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
# ) -> AccountInResponse:
#     try:
#         db_account = await account_repo.read_account_by_id(id=id)
#         access_token = jwt_generator.generate_access_token(account=db_account)

#     except EntityDoesNotExist:
#         raise await http_404_exc_id_not_found_request(id=id)

#     return AccountInResponse(
#         id=db_account.id,
#         authorized_account=AccountWithToken(
#             token=access_token,
#             username=db_account.username,
#             email=db_account.email,  # type: ignore
#             is_verified=db_account.is_verified,
#             is_active=db_account.is_active,
#             is_logged_in=db_account.is_logged_in,
#             created_at=db_account.created_at,
#             updated_at=db_account.updated_at,
#         ),
#     )

# @router.get("/source-account/{client_uuid}")
# async def get_source_account(client_uuid: str):
#     # sAccount = BankService.get_account(client_uuid)
#     # return sAccount.toString()
#     return {"status : 200"}

# @router.post("/transfer-details")
# async def post_transfer_details(request_body: reqTransferDetails):
#     return {"status : 200"}
#     # if BankService.validate_transfer_details(request_body):
#     #     return new WebSocket("ws://localhost:8000/ws")
#     # else:
#     #     return

# @router.post("/transfer-confirm")
# async def post_transfer_details():
#     return {"status : 200"}

# @router.get("/users/{client_uuid}")
# async def read_user(client_uuid: str, db: dbDependency):
#     user = await BankService.get_account(user_id, db)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user