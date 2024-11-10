# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Annotated
# from fastapi.responses import HTMLResponse
# from fastapi.testclient import TestClient
# from datetime import datetime
# # from transformers import pipeline, Conversation

# from service.RetrievalService import RetrievalService as retrieveService
# from service.NLUPreprocessing import nluPreprocessing
# from model.response.GeneralResponse import generalResponse
# from service.ConnectionManagerService import connectionManager
# from controller import BankController, CustomerController

# from fastapi import FastAPI, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from DatabasePostgresConfig import SessionLocal
# from model.Model import Base, engine

# nluService = nluPreprocessing()
# app = FastAPI()
# app.include_router(BankController.router, CustomerController.router)
# manager = connectionManager()


# # FOLLOW THIS DESIGN Pattern
# # https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/main.py

# @app.get("/")
# async def home():
#     websocket_endpoint()

# @app.websocket("/ws-connect/{client_uuid}")
# async def websocket_endpoint(websocket: WebSocket, client_uuid: str):
#     # TODO: sebelum access interrupt and validate user
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_json()
#             user_message = generalResponse(data["message"], data["role"], client_uuid, datetime.now())
            
#             print(user_message.message, user_message.role)

#             user_message = await retrieveService.getRespond(user_message)
#             await manager.send_message(user_message, websocket)
            
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast2(f"Client #{client_uuid} left the chat")

# # Dependency to get the DB session
# async def get_db():
#     async with SessionLocal() as session:
#         yield session

# # Startup event to create the tables
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# dbDependency = Annotated[SessionLocal, Depends(get_db)]