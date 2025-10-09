from typing import List, Optional
from src.schemas.users import UserSchema

# In-memory user storage
users_db: List[UserSchema] = []

def get_user_by_email(email: str) -> Optional[UserSchema]:
    """Find user by email in the in-memory list."""
    return next((user for user in users_db if user.email == email), None)

def get_user_by_id(user_id: int) -> Optional[UserSchema]:
    """Find user by ID in the in-memory list."""
    return next((user for user in users_db if user.user_id == user_id), None)
