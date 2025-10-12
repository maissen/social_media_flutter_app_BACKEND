import pickle
from typing import List, Tuple

from src.schemas.users import UserProfileSchema, UserSearchedSchema
from src.users_crud import get_user_by_id, load_users

DB_FILE = "database/followers_database.dat"

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
    return (user_1, user_2) in followers or (user_2, user_1) in followers



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

    # Update followers count
    increment_followers_count_of_user(user_2)
    
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

    # Update followers count
    decrement_followers_count_of_user(user_2)

    return True


def get_followers_of_user(user_id: int) -> List[UserProfileSchema]:
    """
    Get all users who are following the given user.

    Args:
        user_id (int): The target user's ID.

    Returns:
        List[UserSearchedSchema]: List of followers with basic info.
    """
    # Load followers database
    followers_list = load_followers()
    
    # Find all follower IDs for this user
    follower_ids = [follower_id for (follower_id, following_id) in followers_list if following_id == user_id]

    #
    followers_data: List[UserProfileSchema] = []

    for fid in follower_ids:
        user = get_user_by_id(fid)
        if user:
            followers_data.append(UserProfileSchema(
                user_id=user.user_id,
                email=user.email,
                username=user.username,
                bio=user.bio,
                profile_picture=user.profile_picture,
                followers_count=user.followers_count,
                following_count=user.following_count,
                posts_count=user.posts_count,
                created_at=user.created_at,
                is_following=True
            ))

    return followers_data


def get_followings_of_user(user_id: int) -> List[UserProfileSchema]:
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
    following_data: List[UserProfileSchema] = []

    for fid in following_ids:
        user = get_user_by_id(fid)
        if user:
            following_data.append(UserProfileSchema(
                user_id=user.user_id,
                email=user.email,
                username=user.username,
                bio=user.bio,
                profile_picture=user.profile_picture,
                followers_count=user.followers_count,
                following_count=user.following_count,
                posts_count=user.posts_count,
                created_at=user.created_at,
                is_following=check_following_status(user_1=user_id, user_2=fid)
            ))
            
    return following_data



def increment_followers_count_of_user(user_id: int) -> bool:
    """
    Increment the followers_count of a user by 1.

    Args:
        user_id (int): The ID of the user whose followers count will increase.

    Returns:
        bool: True if successful, False if user not found.
    """
    users = load_users()
    user_found = False

    for user in users:
        if user.user_id == user_id:
            user.followers_count += 1
            user_found = True
            break

    if user_found:
        # Assuming you have a save_users(users) function similar to load_users()
        from src.users_crud import save_users
        save_users(users)
        return True
    
    return False


def decrement_followers_count_of_user(user_id: int) -> bool:
    """
    Decrement the followers_count of a user by 1 (if > 0).

    Args:
        user_id (int): The ID of the user whose followers count will decrease.

    Returns:
        bool: True if successful, False if user not found.
    """
    users = load_users()
    user_found = False

    for user in users:
        if user.user_id == user_id:
            if user.followers_count > 0:
                user.followers_count -= 1
            user_found = True
            break

    if user_found:
        from src.users_crud import save_users
        save_users(users)
        return True
    return False
