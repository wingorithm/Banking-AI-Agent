from fastapi import status, APIRouter, WebSocket, WebSocketDisconnect, Depends
import loguru

from src.model.schemas.request.GlobalRequest import AgentChatRequest
from src.service.AgentService import AgentService


router = APIRouter(prefix="/agent", tags=["agent"])

@router.websocket(
    path="/{customer_id}",
    name="agent:create-web-socket-connection"
)
async def websocket_endpoint(websocket: WebSocket, customer_id: str, agent_service: AgentService = Depends()):
    loguru.logger.info(f"REQUESTING /agent websocket connection")
    await websocket.accept()
    loguru.logger.info(f"CONNECTED session for {customer_id}")
    try:
        while True:
            raw_message = await websocket.receive_text()
            message_data = AgentChatRequest.parse_raw(raw_message)
            response = await agent_service.get_response(customer_id, message_data.message)
            await websocket.send_text(response.json())
    except WebSocketDisconnect:
        loguru.logger.error(f"Client {customer_id} disconnected.")