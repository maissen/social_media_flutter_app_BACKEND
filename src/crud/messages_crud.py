import pickle
from typing import List
from datetime import datetime
from src.schemas.chats import PrivateMessage
from typing import Dict, List
from collections import defaultdict
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


def get_conversations(user_id: int) -> Dict[int, List[PrivateMessage]]:
    """
    Fetch all conversations of a user, grouped by the other participant's user_id.
    Returns:
        A dictionary where:
            - Key: other user's ID
            - Value: list of PrivateMessageSchema objects (sorted by timestamp)
    """
    messages = load_messages()
    conversations: Dict[int, List[PrivateMessage]] = defaultdict(list)

    for msg in messages:
        if msg.sender_id == user_id:
            other_id = msg.recipient_id
        elif msg.recipient_id == user_id:
            other_id = msg.sender_id
        else:
            continue  # Skip messages not involving the user

        # Ensure we always store schema objects
        msg = PrivateMessage(
            sender_id=msg.sender_id,
            recipient_id=msg.recipient_id,
            content=msg.content,
            timestamp=msg.timestamp
        )

        conversations[other_id].append(msg)

    # Sort each conversation by timestamp
    for other_id in conversations:
        conversations[other_id].sort(key=lambda m: m.timestamp)

    return conversations