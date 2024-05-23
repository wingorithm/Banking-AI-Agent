from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from model.response.GeneralResponse import generalResponse
import json

class connectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print(websocket, " Hello")
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, data: generalResponse, websocket: WebSocket):
        print("message check point | message:", data.message, "role:", data.role)
        data2json = {
            "message": data.message,
            "role" : data.role
        }
        json_string = json.dumps(data2json)
        await websocket.send_text(f"{json_string}")
    
    async def broadcast2(self, data: generalResponse):
        for connection in self.active_connections:
            await connection.send_text(f"{data.role}: {data.message}")