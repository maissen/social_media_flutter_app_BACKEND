from pydantic import BaseModel

# Incoming message from a user to another user
class PrivateMessage(BaseModel):
    sender_id: int
    recipient_id: int
    content: str

