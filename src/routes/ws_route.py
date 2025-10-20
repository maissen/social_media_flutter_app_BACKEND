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

                # Send to recipient
                await manager.send_personal_message({
                    "type": "chat",
                    "from": user_id,
                    "content": content
                }, recipient_id)

                # Optional: echo back to sender
                await manager.send_personal_message({
                    "type": "sent",
                    "to": recipient_id,
                    "content": content
                }, user_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)