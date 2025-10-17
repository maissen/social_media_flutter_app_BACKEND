from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.schemas.users import UserProfileSchema
from src.schemas.notification import NotificationSchema


router = APIRouter()


connected_clients: list[tuple[int, WebSocket]] = []  
# Store tuples of (user_id, websocket) to know who is connected

async def connect_client(user_id: int, websocket: WebSocket):
    await websocket.accept()
    connected_clients.append((user_id, websocket))

    print(f"user_id : {user_id} connected {websocket}")


def disconnect_client(websocket: WebSocket):
    global connected_clients
    connected_clients = [(uid, ws) for uid, ws in connected_clients if ws != websocket]

async def broadcast_to_followers_of_user(notification: NotificationSchema, followers: list[UserProfileSchema]):

    follower_ids = [f.user_id for f in followers]

    for uid, ws in connected_clients:
        if uid in follower_ids:
            await ws.send_json(notification)



@router.websocket("/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    """Connect a specific logged-in user"""
    await connect_client(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        disconnect_client(websocket)