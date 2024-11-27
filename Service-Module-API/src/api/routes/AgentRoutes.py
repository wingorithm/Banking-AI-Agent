from fastapi import status, APIRouter, WebSocket, WebSocketDisconnect, Depends
import loguru

from src.model.schemas.request.GlobalRequest import AgentChatRequest
from src.service.AgentService import AgentService
from src.service.IntentClassificationService import IntentClassificationService


router = APIRouter(prefix="/agent", tags=["agent"])

@router.websocket(
    path="/{customer_id}",
    name="agent:create-web-socket-connection"
)
async def websocket_endpoint(
    websocket: WebSocket, 
    customer_id: str, 
    agent_service: AgentService = Depends(), 
    intent_service: IntentClassificationService = Depends()
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
            function_name = await intent_service.classify_intent(customer_id, message_data.message)
            loguru.logger.info(f"Intent classified as: {function_name}")

            # Generate a response based on the intent
            response = await agent_service.get_response(customer_id, message_data.message, function_name)

            # Send response back to the client
            await websocket.send_text(response.json())
    except WebSocketDisconnect:
        loguru.logger.error(f"Client {customer_id} disconnected.")
