import pickle
from datetime import datetime
from typing import List, Optional
from src.schemas.posts import PostSchema, CommentProfile
from src.users_crud import get_user_by_id

POSTS_DB = "database/posts_database.dat"
LIKES_DB = "database/likes_database.dat"
COMMENTS_DB = "database/comments_database.dat" 
FOLLOWERS_DB = "database/followers_database.dat"


# ====================================================
# 🔹 Utility Functions
# ====================================================

def load_pickle(file_path: str):
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def save_pickle(file_path: str, data):
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


# ====================================================
# 🔹 Post CRUD
# ====================================================

def insert_new_post(post: PostSchema) -> PostSchema:
    """Insert a new post into the database."""
    posts = load_pickle(POSTS_DB)
    post.post_id = len(posts) + 1
    posts.append(post)
    save_pickle(POSTS_DB, posts)
    return post


def get_post_by_id(post_id: int) -> Optional[PostSchema]:
    """Retrieve a single post by ID."""
    posts = load_pickle(POSTS_DB)
    return next((p for p in posts if p.post_id == post_id), None)


def get_posts_of_user(current_user_id: int, target_user_id: int) -> List[PostSchema]:
    """Retrieve all posts belonging to a given user, marking which are liked by the current user."""
    posts = load_pickle(POSTS_DB)
    user_posts = [p for p in posts if p.user_id == target_user_id]

    for post in user_posts:
        post.is_liked_by_me = is_post_liked_by_me(current_user_id, post.post_id)

    return user_posts



def delete_a_post(post_id: int) -> bool:
    """Delete a post by ID and clean related likes/comments."""
    posts = load_pickle(POSTS_DB)
    new_posts = [p for p in posts if p.post_id != post_id]
    if len(new_posts) == len(posts):
        return False  # Not found

    save_pickle(POSTS_DB, new_posts)

    # Also remove related likes/comments
    likes = [l for l in load_pickle(LIKES_DB) if l[1] != post_id]
    comments = [c for c in load_pickle(COMMENTS_DB) if getattr(c, "post_id", None) != post_id]
    save_pickle(LIKES_DB, likes)
    save_pickle(COMMENTS_DB, comments)
    return True


def update_a_post(post_id: int, payload: str) -> Optional[PostSchema]:
    """Update the content of an existing post."""
    posts = load_pickle(POSTS_DB)
    for p in posts:
        if p.post_id == post_id:
            p.content = payload
            save_pickle(POSTS_DB, posts)
            return p
    return None


# ====================================================
# 🔹 Likes Management
# ====================================================

def is_post_liked_by_me(user_id: int, post_id: int) -> bool:
    """Check if user liked a given post."""
    likes = load_pickle(LIKES_DB)
    return (user_id, post_id) in likes


def like_post(user_id: int, post_id: int) -> bool:
    """Like a post if not already liked."""
    likes = load_pickle(LIKES_DB)
    if (user_id, post_id) in likes:
        return False

    likes.append((user_id, post_id))
    save_pickle(LIKES_DB, likes)

    # Increment like count in post
    posts = load_pickle(POSTS_DB)
    for p in posts:
        if p.post_id == post_id:
            p.likes_nbr += 1
            break
    save_pickle(POSTS_DB, posts)
    return True


def dislike_post(user_id: int, post_id: int) -> bool:
    """Unlike a post if already liked."""
    likes = load_pickle(LIKES_DB)
    if (user_id, post_id) not in likes:
        return False

    likes.remove((user_id, post_id))
    save_pickle(LIKES_DB, likes)

    # Decrement like count
    posts = load_pickle(POSTS_DB)
    for p in posts:
        if p.post_id == post_id and p.likes_nbr > 0:
            p.likes_nbr -= 1
            break
    save_pickle(POSTS_DB, posts)
    return True


# ====================================================
# 🔹 Comments Management
# ====================================================

def add_comment_to_post(user_id: int, post_id: int, comment_payload: str) -> Optional[CommentProfile]:
    """Add a comment to a post."""
    posts = load_pickle(POSTS_DB)
    if not any(p.post_id == post_id for p in posts):
        return None

    user = get_user_by_id(user_id)
    if not user:
        return None

    comments = load_pickle(COMMENTS_DB)

    new_comment = CommentProfile(
        comment_id=len(comments) + 1,
        user_id=user_id,
        username=user.username,
        profile_picture=user.profile_picture,
        comment_payload=comment_payload,
        created_at=datetime.utcnow()
    )
    comments.append(new_comment)
    save_pickle(COMMENTS_DB, comments)

    # Update post comment counter
    for p in posts:
        if p.post_id == post_id:
            p.comments_nbr += 1
            break
    save_pickle(POSTS_DB, posts)

    return new_comment


def remove_comment_from_post(comment_id: int, post_id: int) -> bool:
    """Remove a comment by ID and update the related post."""
    comments = load_pickle(COMMENTS_DB)
    target_comment = next((c for c in comments if c.comment_id == comment_id), None)
    if not target_comment:
        return False

    comments = [c for c in comments if c.comment_id != comment_id]
    save_pickle(COMMENTS_DB, comments)

    # Decrement post comment counter
    posts = load_pickle(POSTS_DB)
    for p in posts:
        if p.post_id == post_id and p.comments_nbr > 0:
            p.comments_nbr -= 1
            break
    save_pickle(POSTS_DB, posts)

    return True


def get_comments_for_post(post_id: int) -> List[CommentProfile]:
    """Get all comments belonging to a specific post."""
    comments = load_pickle(COMMENTS_DB)
    return [c for c in comments if getattr(c, "post_id", None) == post_id]


# ====================================================
# 🔹 Count Utilities
# ====================================================

def get_posts_count() -> int:
    """
    Get total posts count.
    If user_id is provided → count only that user's posts.
    """
    posts = load_pickle(POSTS_DB)
    return len(posts)


def get_likes_count(post_id: int) -> int:
    """
    Get total likes count.
    - If post_id provided → likes on that post.
    - If user_id provided → likes given by that user.
    """
    likes = load_pickle(LIKES_DB)
    if post_id:
        return sum(1 for (_, pid) in likes if pid == post_id)
    return len(likes)


def get_comments_count(post_id: int) -> int:
    """
    Get total comments count.
    - If post_id provided → comments on that post.
    - If user_id provided → comments made by that user.
    """
    comments = load_pickle(COMMENTS_DB)
    if post_id:
        return sum(1 for c in comments if getattr(c, "post_id", None) == post_id)
    return len(comments)


def increment_comments_count_of_post(post_id: int) -> bool:
    """
    Increment the comments count for a specific post.
    Returns True if successful, False if post not found.
    """
    posts = load_pickle(POSTS_DB)
    for p in posts:
        if p.post_id == post_id:
            p.comments_nbr += 1
            save_pickle(POSTS_DB, posts)
            return True
    return False


def decrement_comments_count_of_post(post_id: int) -> bool:
    """
    Decrement the comments count for a specific post.
    Ensures the count doesn't go below zero.
    Returns True if successful, False if post not found.
    """
    posts = load_pickle(POSTS_DB)
    for p in posts:
        if p.post_id == post_id:
            if p.comments_nbr > 0:
                p.comments_nbr -= 1
            save_pickle(POSTS_DB, posts)
            return True
    return False





def load_posts() -> list[PostSchema]:
    """Load all posts from the posts file."""
    try:
        with open(POSTS_DB, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def load_follows() -> list[dict]:
    """Load all follow relationships from the follows file."""
    try:
        with open(FOLLOWERS_DB, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def load_feed_of_user(user_id: int) -> list[PostSchema]:
    posts = load_posts()
    follows = load_follows()

    # handle both tuple- and dict-based data for safety
    following_ids = []
    for f in follows:
        if isinstance(f, dict):
            if f["follower_id"] == user_id:
                following_ids.append(f["following_id"])
        elif isinstance(f, (tuple, list)) and len(f) >= 2:
            follower_id, following_id = f[0], f[1]
            if follower_id == user_id:
                following_ids.append(following_id)

    # Include current user's own posts
    user_and_following_ids = [user_id] + following_ids

    # Filter posts
    user_feed_posts = [post for post in posts if post.user_id in user_and_following_ids]

    # Sort by creation date (newest first)
    user_feed_posts.sort(key=lambda p: p.created_at, reverse=True)

    return user_feed_posts



def load_recent_posts(limit: int = 20) -> list[PostSchema]:
    """
    Load the most recent posts from all users (for the Explore feed).

    Args:
        limit (int): Number of posts to return. Defaults to 20.

    Returns:
        list[PostSchema]: Most recent posts sorted by creation time (newest first).
    """
    posts = load_posts()

    # Sort by creation time descending
    posts.sort(key=lambda p: p.created_at, reverse=True)

    # Apply limit
    return posts[:limit]
