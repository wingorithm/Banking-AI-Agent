from fastapi import APIRouter, WebSocket
from model.response.SourceAccount import sourceAccount
from model.request.reqTransferDetails import reqTransferDetails
from service.BankService import BankService
from pydantic import BaseModel


router = APIRouter()

@router.get("/source-account/{client_uuid}")
async def get_source_account(client_uuid: str):
    # sAccount = BankService.get_account(client_uuid)
    # return sAccount.toString()
    return {"status : 200"}

@router.post("/transfer-details")
async def post_transfer_details(request_body: reqTransferDetails):
    return {"status : 200"}
    # if BankService.validate_transfer_details(request_body):
    #     return new WebSocket("ws://localhost:8000/ws")
    # else:
    #     return

@router.post("/transfer-confirm")
async def post_transfer_details():
    return {"status : 200"}
