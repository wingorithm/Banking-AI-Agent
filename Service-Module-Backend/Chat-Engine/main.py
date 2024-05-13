from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from ConnectionManager import connectionManager
from fastapi.testclient import TestClient
import time
from transformers import pipeline, Conversation

app = FastAPI()
manager = connectionManager()

@app.get("/")
async def home():
    return HTMLResponse("test")

async def getRespond(user_message : str):

    # chatbot = pipeline(model="facebook/blenderbot-400M-distill")
    # conversation = Conversation(user_message)
    # conversation = await chatbot(conversation)
    # return conversation.messages[-1]["content"]
    response = {"message" : "cape dah", "role" : "bot"}
    return response

@app.websocket("/wsConnect")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_text(f"{data['role']}: {data['message']}")
        response = await getRespond(data['message'])
        await websocket.send_text(f"{response['role']}: {response['message']}")
