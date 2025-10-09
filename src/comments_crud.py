import pickle
from datetime import datetime
from typing import List, Tuple
from src.schemas.posts import CommentProfile

COMMENTS_DB_FILE = "comments_database.dat"
LIKES_DB_FILE = "comments_likes_database.dat"


# ---------- Comments DB ----------
def load_comments() -> List[CommentProfile]:
    try:
        with open(COMMENTS_DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def save_comments(comments: List[CommentProfile]):
    with open(COMMENTS_DB_FILE, "wb") as f:
        pickle.dump(comments, f)

def get_new_comment_id() -> int:
    comments = load_comments()
    if not comments:
        return 1
    return max(comment.comment_id for comment in comments) + 1

def create_comment(current_user, post_id: int, content: str) -> CommentProfile:
    comments = load_comments()
    comment = CommentProfile(
        comment_id=get_new_comment_id(),
        post_id=post_id,
        user_id=current_user.user_id,
        username=current_user.username,
        profile_picture=getattr(current_user, "profile_picture", ""),
        comment_payload=content,
        created_at=datetime.utcnow(),
        likes_nbr=0
    )
    comments.append(comment)
    save_comments(comments)
    return comment

def get_comments_of_post(post_id: int) -> List[CommentProfile]:
    comments = load_comments()
    return [c for c in comments if c.post_id == post_id]

def delete_comment_of_post(comment_id: int, post_id: int) -> bool:
    comments = load_comments()
    updated_comments = [c for c in comments if not (c.comment_id == comment_id and c.post_id == post_id)]
    if len(updated_comments) == len(comments):
        return False
    save_comments(updated_comments)
    
    # Remove likes related to this comment
    likes = load_likes()
    likes = [like for like in likes if like[0] != comment_id]
    save_likes(likes)
    return True


# ---------- Likes DB ----------
def load_likes() -> List[Tuple[int, int]]:
    """Load likes as a list of tuples: (comment_id, user_id)"""
    try:
        with open(LIKES_DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def save_likes(likes: List[Tuple[int, int]]):
    with open(LIKES_DB_FILE, "wb") as f:
        pickle.dump(likes, f)


def like_comment_of_post(comment_id: int, user_id: int) -> bool:
    """Like a comment: increments likes_nbr and adds to likes DB."""
    comments = load_comments()
    likes = load_likes()
    
    # Prevent double-like
    if (comment_id, user_id) in likes:
        return False

    comment = next((c for c in comments if c.comment_id == comment_id), None)
    if not comment:
        return False

    comment.likes_nbr += 1
    likes.append((comment_id, user_id))

    save_comments(comments)
    save_likes(likes)
    return True


def dislike_comment_of_post(comment_id: int, user_id: int) -> bool:
    """Dislike a comment: decrements likes_nbr and removes from likes DB."""
    comments = load_comments()
    likes = load_likes()
    
    if (comment_id, user_id) not in likes:
        return False  # User hasn't liked it

    comment = next((c for c in comments if c.comment_id == comment_id), None)
    if not comment:
        return False

    if comment.likes_nbr > 0:
        comment.likes_nbr -= 1
    likes.remove((comment_id, user_id))

    save_comments(comments)
    save_likes(likes)
    return True


def get_likes_of_comment(comment_id: int) -> int:
    """Return the likes_nbr of a comment."""
    comments = load_comments()
    comment = next((c for c in comments if c.comment_id == comment_id), None)
    return comment.likes_nbr if comment else 0


def get_likes_count_of_comment(comment_id: int) -> int:
    """
    Get the number of likes for a given comment using likes_database.dat.

    Args:
        comment_id (int): ID of the comment.

    Returns:
        int: Number of likes for the comment.
    """
    likes = load_likes()
    return sum(1 for c_id, _ in likes if c_id == comment_id)


def is_comment_liked_by_me(comment_id: int, user_id: int) -> bool:
    """
    Check if the given user has liked a specific comment.

    Args:
        comment_id (int): The ID of the comment.
        user_id (int): The ID of the user.

    Returns:
        bool: True if the user has liked the comment, False otherwise.
    """
    likes = load_likes()
    return (comment_id, user_id) in likes


def increment_likes_count_of_comment(comment_id: int) -> bool:
    """
    Increment the likes_nbr of a comment by 1.

    Args:
        comment_id (int): ID of the comment.

    Returns:
        bool: True if successful, False if comment not found.
    """
    comments = load_comments()
    comment = next((c for c in comments if c.comment_id == comment_id), None)
    if not comment:
        return False

    comment.likes_nbr += 1
    save_comments(comments)
    return True


def decrement_likes_count_of_comment(comment_id: int) -> bool:
    """
    Decrement the likes_nbr of a comment by 1 (minimum 0).

    Args:
        comment_id (int): ID of the comment.

    Returns:
        bool: True if successful, False if comment not found.
    """
    comments = load_comments()
    comment = next((c for c in comments if c.comment_id == comment_id), None)
    if not comment:
        return False

    if comment.likes_nbr > 0:
        comment.likes_nbr -= 1

    save_comments(comments)
    return True


def get_comment_by_id(comment_id: int) -> CommentProfile | None:
    """
    Retrieve a single comment by its ID.

    Args:
        comment_id (int): The ID of the comment.

    Returns:
        CommentProfile | None: The comment if found, otherwise None.
    """
    comments = load_comments()
    return next((c for c in comments if c.comment_id == comment_id), None)
