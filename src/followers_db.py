import pickle
from typing import List, Tuple

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
