from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from src.core.security import get_current_user_from_token
from src.crud.messages_crud import get_conversation, get_conversations, insert_message
from src.crud.users_crud import get_user_by_id
from src.schemas.chats import PrivateMessage, Conversation, SendMessageRequest
from src.schemas.users import UserProfileSimplified
from src.crud.users_crud import get_simplified_user_obj_by_id

router = APIRouter(prefix="", tags=["Messages"])

# ======================
# Send a message
# ======================
@router.post("/send", response_model=PrivateMessage)
def send_message(
    body: SendMessageRequest,
    current_user=Depends(get_current_user_from_token)
):
    # Check if recipient exists
    recipient = get_user_by_id(body.recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    message = insert_message(current_user.user_id, body.recipient_id, body.content)
    return message

# ======================
# Get conversation with a specific user
# ======================
@router.get("/conversation", response_model=Conversation)
def conversation(current_user=Depends(get_current_user_from_token), recipient_id: int = Query(...)):
    # Check if recipient exists
    recipient = get_user_by_id(recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    messages = get_conversation(current_user.user_id, recipient_id)
    return Conversation(participant_id=recipient_id, messages=messages)

# ======================
# Get all conversations of the current user
# ======================
@router.get("/my_conversations", response_model=List[UserProfileSimplified])
def get_my_conversations(current_user=Depends(get_current_user_from_token)):
    """
    Fetch all users the current user has had conversations with.
    """
    raw_conversations = get_conversations(current_user.user_id)  # Should return participant_ids
    users = []

    for conversation in raw_conversations:
        user = get_simplified_user_obj_by_id(user_id=conversation.participant_id)
        if user:
            users.append(user)

    return users
