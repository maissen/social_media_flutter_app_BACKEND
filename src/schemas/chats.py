from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime

class PrivateMessage(BaseModel):
    sender_id: int
    recipient_id: int
    content: str
    timestamp: datetime

class Conversation(BaseModel):
    participant_id: int  # The other user in the conversation
    messages: List[PrivateMessage]  # All messages exchanged with this participant

class ConversationsResponse(BaseModel):
    conversations: Dict[int, List[PrivateMessage]]  # Keyed by participant_id

class SendMessageRequest(BaseModel):
    recipient_id: int
    content: str
