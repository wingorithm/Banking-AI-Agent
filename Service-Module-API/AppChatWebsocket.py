from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient
from datetime import datetime
from transformers import pipeline, Conversation

# from controller import endpoints
from service.RetrievalService import RetrievalService as retrieveService
from service.NLUPreprocessing import nluPreprocessing
from model.response.GeneralResponse import generalResponse
from service.ConnectionManagerService import connectionManager

nluService = nluPreprocessing()
app = FastAPI()
# app.include_router(endpoints.router)
manager = connectionManager()

@app.get("/")
async def home():
    websocket_endpoint()

@app.websocket("/ws-connect/{client_uuid}")
async def websocket_endpoint(websocket: WebSocket, client_uuid: str):
    # TODO: sebelum access interrupt and validate user
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            user_message = generalResponse(data["message"], data["role"], client_uuid, datetime.now())
            
            user_message.setMessage(nluService.preprocessing(user_message.message))

            user_message = await retrieveService.getRespond(user_message)
            await manager.send_message(user_message, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast2(f"Client #{client_uuid} left the chat")
