from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
from src.schemas.users import UserProfileSimplified


class PrivateMessage(BaseModel):
    sender_id: int
    recipient_id: int
    content: str
    is_read: bool = False
    timestamp: datetime

class Conversation(BaseModel):
    participant_id: int  # The other user in the conversation
    messages: List[PrivateMessage]  # All messages exchanged with this participant

class SendMessageRequest(BaseModel):
    recipient_id: int
    content: str
