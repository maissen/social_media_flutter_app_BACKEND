import pickle
from typing import List, Tuple, Optional
from src.schemas.users import UserSchema, UserProfileSchema, UpdateBioRequest, UpdateProfilePictureRequest

USERS_DB_FILE = "database/users_database.dat"
DB_FILE = "database/followers_database.dat"

# ======================
# Users CRUD
# ======================

def load_users() -> list[UserSchema]:
    """Load users from the file."""
    try:
        with open(USERS_DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []
    
def generate_new_user_id():
    return len(load_users()) + 1

def save_users(users: list[UserSchema]):
    """Save users to the file."""
    with open(USERS_DB_FILE, "wb") as f:
        pickle.dump(users, f)

def get_user_by_email(email: str) -> Optional[UserSchema]:
    """Find user by email in the file-based users list."""
    users = load_users()
    return next((user for user in users if user.email == email), None)

def get_user_by_id(user_id: int) -> Optional[UserSchema]:
    """Find user by ID in the file-based users list."""
    users = load_users()
    return next((user for user in users if user.user_id == user_id), None)

from src.schemas.users import UserSchema, UserProfileSimplified
from typing import Optional

def get_simplified_user_obj_by_id(user_id: int) -> Optional[UserProfileSimplified]:
    """
    Retrieve a simplified user profile by user_id.
    Returns UserProfileSimplified or None if user not found.
    """
    user: UserSchema = get_user_by_id(user_id)
    if not user:
        return None

    simplified_user = UserProfileSimplified(
        user_id=user.user_id,
        email=user.email,
        username=user.username,
        profile_picture=user.profile_picture,
        is_following=user.is_following
    )
    return simplified_user


def insert_new_user(user: UserSchema):
    """Insert a new user into the file-based database."""
    users = load_users()
    users.append(user)
    save_users(users)

def update_user_bio(user_id: int, payload: UpdateBioRequest) -> Optional[UserSchema]:
    """Update a user's bio and save to file."""
    users = load_users()
    for user in users:
        if user.user_id == user_id:
            user.bio = payload
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

def find_matching_username(current_user: int, username: str) -> List[UserSchema]:
    """Search for users whose username starts with the search string (case-insensitive)."""
    username = username.lower()
    users = load_users()
    matching_users = [
        user for user in users if user.username.lower().startswith(username)
    ]

    for user in matching_users:
        user.is_following = check_following_status(user_1=current_user, user_2=user.user_id)

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

def update_user_profile_picture(file: str, user_id: int) -> Optional[UserSchema]:
    """Update a user's profile picture with the given file path or filename."""
    users = load_users()
    for user in users:
        if user.user_id == user_id:
            user.profile_picture = file
            save_users(users)
            return user
    return None  # User not found


# ======================
# Followers CRUD
# ======================

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
    """Check if user_1 is following user_2."""
    followers = load_followers()
    return (user_1, user_2) in followers


def follow(user_1: int, user_2: int) -> bool:
    """Make user_1 follow user_2."""
    if user_1 == user_2:
        return False  # Cannot follow oneself
    
    followers = load_followers()
    if (user_1, user_2) in followers:
        return False  # Already following

    followers.append((user_1, user_2))
    save_followers(followers)

    increment_followers_count_of_user(user_2)
    return True

def unfollow(user_1: int, user_2: int) -> bool:
    """Make user_1 unfollow user_2."""
    followers = load_followers()
    if (user_1, user_2) not in followers:
        return False  # Not following
    
    followers.remove((user_1, user_2))
    save_followers(followers)

    decrement_followers_count_of_user(user_2)
    return True

def get_followers_of_user(user_id: int) -> List[UserProfileSchema]:
    """Get all users who are following the given user."""
    followers_list = load_followers()
    follower_ids = [follower_id for (follower_id, following_id) in followers_list if following_id == user_id]

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
    """Get all users that the given user is following."""
    followers_list = load_followers()
    following_ids = [following_id for (follower_id, following_id) in followers_list if follower_id == user_id]

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
    """Increment the followers_count of a user by 1."""
    users = load_users()
    user_found = False

    for user in users:
        if user.user_id == user_id:
            user.followers_count += 1
            user_found = True
            break

    if user_found:
        save_users(users)
        return True
    
    return False

def decrement_followers_count_of_user(user_id: int) -> bool:
    """Decrement the followers_count of a user by 1 (if > 0)."""
    users = load_users()
    user_found = False

    for user in users:
        if user.user_id == user_id:
            if user.followers_count > 0:
                user.followers_count -= 1
            user_found = True
            break

    if user_found:
        save_users(users)
        return True
    return False
