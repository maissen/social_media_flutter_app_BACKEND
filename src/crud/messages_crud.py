import pickle
from typing import List
from datetime import datetime
from src.schemas.chats import PrivateMessage

MESSAGES_DB_FILE = "database/messages_database.dat"


def load_messages() -> List[PrivateMessage]:
    """Load all messages from the file."""
    try:
        with open(MESSAGES_DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def save_messages(messages: List[PrivateMessage]):
    """Save all messages to the file."""
    with open(MESSAGES_DB_FILE, "wb") as f:
        pickle.dump(messages, f)

def insert_message(sender_id: int, recipient_id: int, content: str) -> PrivateMessage:
    """Insert a new message between users."""
    messages = load_messages()
    message = PrivateMessage(
        sender_id=sender_id,
        recipient_id=recipient_id,
        content=content,
        timestamp=datetime.utcnow()
    )
    messages.append(message)
    save_messages(messages)
    return message

def get_conversation(user_1: int, user_2: int) -> List[PrivateMessage]:
    """Retrieve all messages exchanged between two users, sorted by timestamp."""
    messages = load_messages()
    conversation = [
        msg for msg in messages
        if (msg.sender_id == user_1 and msg.recipient_id == user_2) or
           (msg.sender_id == user_2 and msg.recipient_id == user_1)
    ]
    return sorted(conversation, key=lambda msg: msg.timestamp)