import pickle
from typing import Optional
from src.schemas.users import UserSchema

DB_FILE = "users_database.dat"

def load_users() -> list[UserSchema]:
    """Load users from the file."""
    try:
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def get_user_by_email(email: str) -> Optional[UserSchema]:
    """Find user by email in the file-based users list."""
    users = load_users()
    return next((user for user in users if user.email == email), None)

def get_user_by_id(user_id: int) -> Optional[UserSchema]:
    """Find user by ID in the file-based users list."""
    users = load_users()
    return next((user for user in users if user.user_id == user_id), None)

def insert_user(user: UserSchema):
    """Insert a new user into the file-based database."""
    users = load_users()  # Load existing users
    users.append(user)    # Add the new user
    with open(DB_FILE, "wb") as f:
        pickle.dump(users, f)  # Save updated list back to file