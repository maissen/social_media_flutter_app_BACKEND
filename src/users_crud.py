import pickle
from typing import List, Optional
from src.schemas.users import UserSchema, UpdateBioRequest, UpdateProfilePictureRequest

DB_FILE = "users_database.dat"

def load_users() -> list[UserSchema]:
    """Load users from the file."""
    try:
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []
    
def get_new_user_id():
    return len(load_users()) + 1

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


def find_matching_username(username: str) -> List[UserSchema]:
    """
    Search for users whose username contains the username (case-insensitive).

    Args:
        username (str): Substring to search for in usernames.

    Returns:
        List[UserSchema]: List of matching users.
    """
    username = username.lower()
    users = load_users()
    matching_users = [user for user in users if username in user.username.lower()]
    return matching_users


def increment_posts_count_of_user(user_id: int) -> Optional[UserSchema]:
    """Increment the post count of a user by 1."""
    users = load_users()
    for user in users:
        if user.user_id == user_id:
            user.posts_count += 1
            save_users(users)
            return user
    return None  # User not found


def decrement_posts_count_of_user(user_id: int) -> Optional[UserSchema]:
    """Decrement the post count of a user by 1 (not below 0)."""
    users = load_users()
    for user in users:
        if user.user_id == user_id:
            user.posts_count = max(0, user.posts_count - 1)
            save_users(users)
            return user
    return None  # User not found
