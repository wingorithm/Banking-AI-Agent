from fastapi import status, APIRouter, WebSocket, WebSocketDisconnect, Depends
import loguru

from src.model.schemas.request.GlobalRequest import AgentChatRequest
from src.api.dependencies.service import get_agent_service, get_intent_classification_service, get_bank_service
from src.service.AgentService import AgentService
from src.service.IntentClassificationService import IntentClassificationService
from src.service.BankService import BankService


router = APIRouter(prefix="/agent", tags=["agent"])

@router.websocket(
    path="/{customer_id}",
    name="agent:create-web-socket-connection"
)
async def websocket_endpoint(
    websocket: WebSocket, 
    customer_id: str,
    agent_service: AgentService = Depends(get_agent_service),
    intent_classification_service: IntentClassificationService = Depends(get_intent_classification_service),
    bank_service: BankService = Depends(get_bank_service)
):
    loguru.logger.info(f"REQUESTING /agent websocket connection")
    await websocket.accept()
    loguru.logger.info(f"CONNECTED session for {customer_id}")
    try:
        while True:
            # Receive and parse incoming message
            raw_message = await websocket.receive_text()
            message_data = AgentChatRequest.parse_raw(raw_message)

            # Classify the intent of the customer's message
            function_name = await intent_classification_service.classify_intent(customer_id=customer_id, user_message=message_data.message)
            loguru.logger.info(f"Intent classified as: {function_name}")

            # Generate a response based on the intent / save action to job queue
            response = await agent_service.get_response(customer_id, message_data.message, function_name)

            # Get customer data (based on action) [OPTIONAL]
            data = await bank_service.get_data(customer_id, function_name)
            if data:
                response.data = data

            # Send response back to the client
            await websocket.send_text(response.json())
    except WebSocketDisconnect:
        loguru.logger.error(f"Client {customer_id} disconnected.")
