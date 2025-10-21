from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from src.core.ws_manager import manager


router = APIRouter(prefix="", tags=["websocket"])

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, user_id: int = Query(...)):
    """
    WebSocket connection for a user.
    Connect with: ws://localhost:8000/ws?user_id=123
    """
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "chat":
                recipient_id = data.get("recipient_id")
                content = data.get("content")

                print(f"sender : {user_id}, receiver : {recipient_id}")

                # 1. Save message to database/pickle
                from src.crud.messages_crud import insert_message
                insert_message(sender_id=user_id, recipient_id=recipient_id, content=content)
                print("message is inserted")

                # 2. Send to recipient
                await manager.send_personal_message({
                    "type": "chat",
                    "from": user_id,
                    "content": content
                }, recipient_id)

                # 3. Echo back to sender
                await manager.send_personal_message({
                    "type": "sent",
                    "to": recipient_id,
                    "content": content
                }, user_id)

            if msg_type == "typing":
                recipient_id = data.get("recipient_id")
                status = data.get("status")  # "start" or "stop"

                # Send typing status to recipient
                await manager.send_personal_message({
                    "type": "typing",
                    "from": user_id,
                    "status": status
                }, recipient_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)