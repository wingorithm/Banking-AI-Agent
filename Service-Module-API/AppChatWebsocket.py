from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient
import time
from transformers import pipeline, Conversation

from controller import endpoints
from service.RetrievalService import RetrievalService
from model.response.GeneralResponse import generalResponse
from service.ConnectionManagerService import connectionManager

app = FastAPI()
app.include_router(endpoints.router)
manager = connectionManager()
retrieve = RetrievalService

@app.get("/")
async def home():
    websocket_endpoint()

@app.websocket("/ws-connect/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # TODO: sebelum access interrupt and validate user
    await manager.connect(websocket)
    try:
        while True:
            # TODO: Retriece string decode jadi json
            data = websocket.receive() 

            # await websocket.receive_json()
            user_message = generalResponse(data["message"], data["role"])
            await manager.send_message(user_message, websocket)

            # TODO: sebelum response preprocessing dulu
            respose = await retrieve.getRespond(data, client_id)
            await manager.broadcast(respose, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")