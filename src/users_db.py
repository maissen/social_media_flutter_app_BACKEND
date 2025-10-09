import pickle
from typing import Optional
from src.schemas.users import UserSchema, UpdateBioRequest, UpdateProfilePictureRequest

DB_FILE = "users_database.dat"

def load_users() -> list[UserSchema]:
    """Load users from the file."""
    try:
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def save_users(users: list[UserSchema]):
    """Save users to the file."""
    with open(DB_FILE, "wb") as f:
        pickle.dump(users, f)

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
    users = load_users()
    users.append(user)
    save_users(users)

def update_user_bio(user_id: int, payload: UpdateBioRequest) -> Optional[UserSchema]:
    """Update a user's bio and save to file."""
    users = load_users()
    for user in users:
        if user.user_id == user_id:
            user.bio = payload.new_bio
            save_users(users)
            return user
    return None  # User not found

def update_user_profile_picture(user_id: int, payload: UpdateProfilePictureRequest) -> Optional[UserSchema]:
    """Update a user's profile picture and save to file."""
    users = load_users()
    for user in users:
        if user.user_id == user_id:
            user.profile_picture = payload.profile_picture
            save_users(users)
            return user
    return None  # User not found
