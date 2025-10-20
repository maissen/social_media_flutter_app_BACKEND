from http.client import HTTPException
from src.crud.messages_crud import get_conversation, insert_message
from src.crud.users_crud import get_user_by_id
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import json
from schemas.chats import PrivateMessage
from src.core.ws_manager import manager

router = APIRouter(prefix="", tags=["Messages"])

# ======================
# Send a message
# ======================
@router.post("/", response_model=PrivateMessage)
def send_message(sender_id: int, recipient_id: int, content: str):
    # Check if users exist
    sender = get_user_by_id(sender_id)
    recipient = get_user_by_id(recipient_id)
    if not sender or not recipient:
        raise HTTPException(status_code=404, detail="Sender or recipient not found")

    message = insert_message(sender_id, recipient_id, content)
    return message

# ======================
# Get conversation
# ======================
@router.get("/{user_1}/{user_2}", response_model=List[PrivateMessage])
def conversation(user_1: int, user_2: int):
    # Check if users exist
    user_a = get_user_by_id(user_1)
    user_b = get_user_by_id(user_2)
    if not user_a or not user_b:
        raise HTTPException(status_code=404, detail="One or both users not found")

    messages = get_conversation(user_1, user_2)
    return messages



@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = PrivateMessage(**json.loads(data))

                # Send the message to the recipient if they're connected
                await manager.send_personal_message({
                    "type": "private_message",
                    "sender_id": msg.sender_id,
                    "content": msg.content
                }, msg.recipient_id)

            except Exception as e:
                # Could not parse message, ignore or log
                print(f"Failed to handle message: {e}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
