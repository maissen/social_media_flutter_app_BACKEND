import pickle
from datetime import datetime
from typing import List, Dict
from src.schemas.posts import CommentProfile

DB_FILE = "comments_database.dat"

def load_comments() -> List[CommentProfile]:
    """Load all comments from the file."""
    try:
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def save_comments(comments: List[CommentProfile]):
    """Save all comments to the file."""
    with open(DB_FILE, "wb") as f:
        pickle.dump(comments, f)

def get_new_comment_id() -> int:
    """Generate a new comment ID."""
    comments = load_comments()
    if not comments:
        return 1
    return max(comment.comment_id for comment in comments) + 1

def create_comment(current_user, post_id: int, content: str) -> CommentProfile:
    """Create a new comment on a post."""
    comments = load_comments()
    comment = CommentProfile(
        comment_id=get_new_comment_id(),
        user_id=current_user.user_id,
        username=current_user.username,
        profile_picture=getattr(current_user, "profile_picture", ""),
        comment_payload=content,
        created_at=datetime.utcnow()
    )
    comments.append(comment)
    save_comments(comments)
    return comment

def get_comments_of_post(post_id: int) -> List[CommentProfile]:
    """Retrieve all comments for a given post."""
    comments = load_comments()
    return [c for c in comments if c.post_id == post_id]  # Assuming CommentProfile has post_id

def delete_comment_of_post(comment_id: int, post_id: int) -> bool:
    """Delete a specific comment of a post."""
    comments = load_comments()
    updated_comments = [c for c in comments if not (c.comment_id == comment_id and c.post_id == post_id)]
    if len(updated_comments) == len(comments):
        return False  # Comment not found
    save_comments(updated_comments)
    return True

# For likes/dislikes, we'll maintain a dictionary inside each comment: liked_by: set[user_id]
def like_comment_of_post(comment_id: int, user_id: int) -> bool:
    """Like a comment."""
    comments = load_comments()
    for c in comments:
        if c.comment_id == comment_id:
            if not hasattr(c, "liked_by"):
                c.liked_by = set()
            c.liked_by.add(user_id)
            save_comments(comments)
            return True
    return False

def dislike_comment_of_post(comment_id: int, user_id: int) -> bool:
    """Remove a like from a comment."""
    comments = load_comments()
    for c in comments:
        if c.comment_id == comment_id and hasattr(c, "liked_by"):
            c.liked_by.discard(user_id)
            save_comments(comments)
            return True
    return False


def get_likes_of_comment(comment_id: int) -> int:
    """
    Get the number of likes for a given comment.

    Args:
        comment_id (int): ID of the comment.

    Returns:
        int: Number of likes if comment exists, otherwise None
    """
    comments = load_comments()
    comment = next((c for c in comments if c.comment_id == comment_id), None)
    if comment:
        return comment.likes_nbr
    return 0



