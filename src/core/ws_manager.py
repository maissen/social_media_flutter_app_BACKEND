from fastapi import WebSocket
from typing import Dict
import asyncio

class ConnectionManager:
    def __init__(self):
        # Maps user_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}
        # Maps websocket object ID -> user_id
        self.websocket_to_user: Dict[int, int] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        """Accept and register a new websocket connection."""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.websocket_to_user[id(websocket)] = user_id

        print(f"[+] User {user_id} connected. Total active: {len(self.active_connections)}")
        await self.broadcast_user_list()

    def disconnect(self, websocket: WebSocket):
        """Remove websocket from tracking after disconnect."""
        ws_id = id(websocket)
        if ws_id in self.websocket_to_user:
            user_id = self.websocket_to_user[ws_id]
            del self.websocket_to_user[ws_id]
            if user_id in self.active_connections:
                del self.active_connections[user_id]
            print(f"[-] User {user_id} disconnected. Remaining users: {list(self.active_connections.keys())}")
        else:
            print("[!] Unknown websocket disconnected.")
        # Broadcast user list asynchronously
        asyncio.create_task(self.broadcast_user_list())

    async def send_personal_message(self, message: dict, user_id: int):
        """Send a message to a specific user if connected."""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
                print(f"[>] Sent message to User {user_id}: {message}")
            except Exception as e:
                print(f"[x] Failed to send message to User {user_id}: {e}")
        else:
            print(f"[!] User {user_id} not connected. Message not sent.")

    async def broadcast_user_list(self):
        """Send the list of all currently connected users to everyone."""
        users = list(self.active_connections.keys())
        message = {
            "type": "user_list",
            "users": users
        }
        print(f"[=] Broadcasting user list: {users}")
        await self.broadcast(message)

    async def broadcast(self, message: dict):
        """Send a message to all connected users."""
        disconnected = []
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"[x] Broadcast failed for User {user_id}: {e}")
                disconnected.append(user_id)

        # Clean up any dead connections
        for user_id in disconnected:
            if user_id in self.active_connections:
                del self.active_connections[user_id]
                print(f"[!] Cleaned up dead connection for User {user_id}")

        if disconnected:
            print(f"[=] Active users after cleanup: {list(self.active_connections.keys())}")


manager = ConnectionManager()
