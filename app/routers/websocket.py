# app/routes/websocket_routes.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

# WebSocket router instance
websocket_router = APIRouter()

# Connection manager to keep track of active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

# Create a manager instance
manager = ConnectionManager()

# WebSocket endpoint for notifications
@websocket_router.websocket("/ws/notify")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keeps connection open
    except WebSocketDisconnect:
        manager.disconnect(websocket)
