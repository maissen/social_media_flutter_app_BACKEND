from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.websocket_to_user: Dict[int, int] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.websocket_to_user[id(websocket)] = user_id
        await self.broadcast_user_list()

    def disconnect(self, websocket: WebSocket):
        ws_id = id(websocket)
        if ws_id in self.websocket_to_user:
            user_id = self.websocket_to_user[ws_id]
            del self.websocket_to_user[ws_id]
            if user_id in self.active_connections:
                del self.active_connections[user_id]
        asyncio.create_task(self.broadcast_user_list())

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except:
                pass

    async def broadcast_user_list(self):
        users = list(self.active_connections.keys())
        message = {
            "type": "user_list",
            "users": users
        }
        await self.broadcast(message)

    async def broadcast(self, message: dict):
        disconnected = []
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except:
                disconnected.append(user_id)

        for user_id in disconnected:
            if user_id in self.active_connections:
                del self.active_connections[user_id]

manager = ConnectionManager()
