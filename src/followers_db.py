import pickle
from typing import List, Tuple

from src.schemas.users import UserSearchedSchema
from src.users_db import get_user_by_id, load_users

DB_FILE = "followers_database.dat"

# Each entry is a tuple: (follower_id, following_id)
# Example: (1, 2) means user 1 follows user 2

def load_followers() -> List[Tuple[int, int]]:
    """Load the followers database from file."""
    try:
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def save_followers(followers: List[Tuple[int, int]]):
    """Save the followers database to file."""
    with open(DB_FILE, "wb") as f:
        pickle.dump(followers, f)

def check_following_status(user_1: int, user_2: int) -> bool:
    """
    Check if user_1 is following user_2.

    Returns:
        True if following, False otherwise
    """
    followers = load_followers()
    return (user_1, user_2) in followers

def follow(user_1: int, user_2: int) -> bool:
    """
    Make user_1 follow user_2.

    Returns:
        True if follow successful, False if already following
    """
    if user_1 == user_2:
        return False  # Cannot follow oneself
    
    followers = load_followers()
    if (user_1, user_2) in followers:
        return False  # Already following

    followers.append((user_1, user_2))
    save_followers(followers)
    return True

def unfollow(user_1: int, user_2: int) -> bool:
    """
    Make user_1 unfollow user_2.

    Returns:
        True if unfollow successful, False if not following
    """
    followers = load_followers()
    if (user_1, user_2) not in followers:
        return False  # Not following
    
    followers.remove((user_1, user_2))
    save_followers(followers)
    return True


def get_followers_of_user(user_id: int) -> List[UserSearchedSchema]:
    """
    Get all users who are following the given user.

    Args:
        user_id (int): The target user's ID.

    Returns:
        List[UserSearchedSchema]: List of followers with basic info.
    """
    from followers_db import load_followers  # Ensure we use the correct DB
    
    # Load followers database
    followers_list = load_followers()
    
    # Find all follower IDs for this user
    follower_ids = [follower_id for (follower_id, following_id) in followers_list if following_id == user_id]

    # Load all users
    users = load_users()

    # Build response with minimal info (UserSearchedSchema)
    followers_data: List[UserSearchedSchema] = []
    for fid in follower_ids:
        user = get_user_by_id(fid)
        if user:
            followers_data.append(UserSearchedSchema(
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                profile_picture=user.profile_picture
            ))
    return followers_data


def get_followings_of_user(user_id: int) -> List[UserSearchedSchema]:
    """
    Get all users that the given user is following.

    Args:
        user_id (int): The user's ID.

    Returns:
        List[UserSearchedSchema]: List of users being followed with basic info.
    """
    # Load followers database
    followers_list = load_followers()
    
    # Find all following IDs for this user
    following_ids = [following_id for (follower_id, following_id) in followers_list if follower_id == user_id]

    # Build response with minimal info (UserSearchedSchema)
    following_data: List[UserSearchedSchema] = []
    for fid in following_ids:
        user = get_user_by_id(fid)
        if user:
            following_data.append(UserSearchedSchema(
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                profile_picture=user.profile_picture
            ))
    return following_data