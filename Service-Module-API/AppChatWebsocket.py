from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient
import time
from transformers import pipeline, Conversation

from service.RetrievalService import RetrievalService
from model.response.GeneralResponse import generalResponse
from service.ConnectionManagerService import connectionManager

app = FastAPI()
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
            # data = await websocket.receive_json()
            data = await websocket.receive_json()
            print("Here's my Data -> ", data)
            user_message = generalResponse(data["message"], data["role"])
            print("Here's my Data -> ", user_message.message , " <> ", user_message.role)
            # await manager.send_message(user_message, websocket)
            # TODO: sebelum response preprocessing dulu
            respose = await retrieve.getRespond(data, client_id)
            await manager.broadcast(respose, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast2(f"Client #{client_id} left the chat")
