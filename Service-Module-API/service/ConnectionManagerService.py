from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from model.response.GeneralResponse import generalResponse

class connectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print(websocket)
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, data: generalResponse, websocket: WebSocket):
        await websocket.send_text(f"{data.role}: {data.message}")

    async def broadcast(self, data: generalResponse, websocket: WebSocket):
        await websocket.send_text(f"{data.role}: {data.message}")
        # for connection in self.active_connections:
        #     await connection.send_text(f"{data.role}: {data.message}")
