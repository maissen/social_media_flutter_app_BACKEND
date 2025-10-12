import pickle
from datetime import datetime
from typing import List, Optional, Tuple
from src.schemas.posts import PostSchema, CommentProfile
from src.crud.users_crud import get_user_by_id, USERS_DB_FILE


# ====================================================
# 🔹 Database File Paths
# ====================================================

POSTS_DB = "database/posts_database.dat"
LIKES_DB = "database/likes_database.dat"
COMMENTS_DB = "database/comments_database.dat"
FOLLOWERS_DB = "database/followers_database.dat"
COMMENTS_DB_FILE = "database/comments_database.dat"
LIKES_DB_FILE = "database/comments_likes_database.dat"


# ====================================================
# 🔹 Utility Functions
# ====================================================

def load_data_from_dat_file(file_path: str):
    try:
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def save_data_to_dat_file(file_path: str, data):
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


# ====================================================
# 🔹 Post CRUD
# ====================================================

def get_post_by_id(post_id: int) -> Optional[PostSchema]:
    posts = load_data_from_dat_file(POSTS_DB)
    return next((p for p in posts if p.post_id == post_id), None)



def create_new_post(post: PostSchema) -> Optional[PostSchema]:

    posts = load_data_from_dat_file(POSTS_DB)
    post.post_id = len(posts) + 1
    posts.append(post)

    increment_posts_count_of_user(user_id=post.user_id)

    save_data_to_dat_file(POSTS_DB, posts)
    return post



def get_posts_of_user(current_user_id: int, target_user_id: int) -> List[PostSchema]:

    posts = load_data_from_dat_file(POSTS_DB)
    user_posts = [p for p in posts if p.user_id == target_user_id]
    
    for post in user_posts:
        post.is_liked_by_me = is_post_liked_by_me(current_user_id, post.post_id)
    
    return user_posts


def delete_a_post(post_id: int) -> bool:

    posts = load_data_from_dat_file(POSTS_DB)
    new_posts = [p for p in posts if p.post_id != post_id]

    if len(new_posts) == len(posts):
        return False
    
    decrement_posts_count_of_user(user_id=get_post_by_id(post_id).user_id)
    
    save_data_to_dat_file(POSTS_DB, new_posts)
    return True



def update_a_post(post_id: int, payload: str) -> Optional[PostSchema]:

    posts = load_data_from_dat_file(POSTS_DB)

    for p in posts:
        if p.post_id == post_id:
            p.content = payload
            save_data_to_dat_file(POSTS_DB, posts)
            return p

    return None


# ====================================================
# 🔹 User Post Count Utilities
# ====================================================

def increment_posts_count_of_user(user_id: int) -> bool:
    """
    Increment the number of posts for a given user.
    Returns True if successful, False otherwise.
    """
    users = load_data_from_dat_file(USERS_DB_FILE)

    user = get_user_by_id(user_id)
    if not user:
        return False

    user.posts_count += 1

    # Update user in list
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users[i] = user
            break

    save_data_to_dat_file(USERS_DB_FILE, users)
    return True


def decrement_posts_count_of_user(user_id: int) -> bool:
    """
    Decrement the number of posts for a given user.
    Ensures the count does not go below zero.
    Returns True if successful, False otherwise.
    """
    users = load_data_from_dat_file(USERS_DB_FILE)

    user = get_user_by_id(user_id)
    if not user:
        return False

    if user.posts_count > 0:
        user.posts_count -= 1

    # Update user in list
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users[i] = user
            break

    save_data_to_dat_file(USERS_DB_FILE, users)
    return True


# ====================================================
# 🔹 Likes Management (Posts)
# ====================================================

def is_post_liked_by_me(user_id: int, post_id: int) -> bool:
    likes = load_data_from_dat_file(LIKES_DB)
    return (user_id, post_id) in likes


def like_post(user_id: int, post_id: int) -> bool:

    if is_post_liked_by_me(user_id, post_id):
        return False
    
    likes = load_data_from_dat_file(LIKES_DB)
    likes.append((user_id, post_id))

    save_data_to_dat_file(LIKES_DB, likes)

    increment_likes_count_of_post(post_id=post_id)
    return True


def dislike_post(user_id: int, post_id: int) -> bool:

    likes = load_data_from_dat_file(LIKES_DB)
    if (user_id, post_id) not in likes:
        return False
    
    likes.remove((user_id, post_id))

    save_data_to_dat_file(LIKES_DB, likes)
    
    decrement_likes_count_of_post(post_id=post_id)
    return True


# ====================================================
# 🔹 Comments Management (Posts)
# ====================================================

def add_comment_to_post(user_id: int, post_id: int, comment_payload: str) -> Optional[CommentProfile]:

    if get_post_by_id(post_id) is None:
        return None
    
    user = get_user_by_id(user_id)
    if user is None:
        return None
    
    comments = load_data_from_dat_file(COMMENTS_DB)
    new_comment = CommentProfile(
        comment_id=len(comments) + 1,
        post_id=post_id,
        user_id=user_id,
        username=user.username,
        profile_picture=user.profile_picture,
        comment_payload=comment_payload,
        created_at=datetime.utcnow(),
        likes_nbr=0,
        is_liked_by_me=False
    )

    print(f"the actual comment is : {new_comment.comment_payload}")
    
    comments.append(new_comment)
    save_data_to_dat_file(COMMENTS_DB, comments)
    
    increment_comments_count_of_post(post_id)
    return new_comment



def remove_comment_from_post(comment_id: int, post_id: int) -> bool:

    comments = load_data_from_dat_file(COMMENTS_DB)
    target_comment = get_comment_by_id(comment_id=comment_id)

    if not target_comment:
        return False
    
    comments = [c for c in comments if c.comment_id != comment_id]
    save_data_to_dat_file(COMMENTS_DB, comments)

    decrement_comments_count_of_post(post_id)
    return True



def get_comments_of_post(post_id: int) -> List[CommentProfile]:
    comments = load_data_from_dat_file(COMMENTS_DB)
    return [c for c in comments if getattr(c, "post_id", None) == post_id]


# ====================================================
# 🔹 Count Utilities (Posts)
# ====================================================

def increment_comments_count_of_post(post_id: int) -> bool:
    posts = load_data_from_dat_file(POSTS_DB)
    for p in posts:
        if p.post_id == post_id:
            p.comments_nbr += 1
            save_data_to_dat_file(POSTS_DB, posts)
            return True
    return False


def decrement_comments_count_of_post(post_id: int) -> bool:
    posts = load_data_from_dat_file(POSTS_DB)
    for p in posts:
        if p.post_id == post_id:
            if p.comments_nbr > 0:
                p.comments_nbr -= 1
            save_data_to_dat_file(POSTS_DB, posts)
            return True
    return False


def increment_likes_count_of_post(post_id: int) -> bool:

    posts = load_data_from_dat_file(POSTS_DB)

    for p in posts:
        if p.post_id == post_id:
            p.likes_nbr += 1
            save_data_to_dat_file(POSTS_DB, posts)
            return True
        
    return False


def decrement_likes_count_of_post(post_id: int) -> bool:
    posts = load_data_from_dat_file(POSTS_DB)
    for p in posts:
        if p.post_id == post_id:
            if p.likes_nbr > 0:
                p.likes_nbr -= 1
            save_data_to_dat_file(POSTS_DB, posts)
            return True
    return False


# ====================================================
# 🔹 Feed and Follows
# ====================================================

def load_posts() -> list[PostSchema]:
    try:
        with open(POSTS_DB, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def load_follows() -> list[dict]:
    try:
        with open(FOLLOWERS_DB, "rb") as f:
            return pickle.load(f)
        
    except (FileNotFoundError, EOFError):
        return []


def load_feed_of_user(user_id: int) -> list[PostSchema]:

    posts = load_posts()
    follows = load_follows()
    following_ids = []
    
    for f in follows:
        if isinstance(f, dict):
            if f["follower_id"] == user_id:
                following_ids.append(f["following_id"])
        elif isinstance(f, (tuple, list)) and len(f) >= 2:
            follower_id, following_id = f[0], f[1]
            if follower_id == user_id:
                following_ids.append(following_id)
    
    user_and_following_ids = [user_id] + following_ids
    user_feed_posts = [post for post in posts if post.user_id in user_and_following_ids]
    user_feed_posts.sort(key=lambda p: p.created_at, reverse=True)
    
    return user_feed_posts


def load_recent_posts(limit: int = 20) -> list[PostSchema]:
    posts = load_posts()
    posts.sort(key=lambda p: p.created_at, reverse=True)
    return posts[:limit]


# ====================================================
# 🔹 Comments DB Management (Independent)
# ====================================================

def load_comments() -> List[CommentProfile]:
    try:
        with open(COMMENTS_DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def save_comments(comments: List[CommentProfile]):
    with open(COMMENTS_DB_FILE, "wb") as f:
        pickle.dump(comments, f)


def get_comments_of_post(post_id: int, current_user_id: int) -> List[CommentProfile]:
    all_comments = load_comments()
    needed_comments = [c for c in all_comments if c.post_id == post_id]

    for c in needed_comments:
        c.is_liked_by_me = is_comment_liked_by_me(comment_id=c.comment_id, user_id=current_user_id)

    return needed_comments


# ====================================================
# 🔹 Likes Management (Comments)
# ====================================================

def load_comment_likes() -> List[Tuple[int, int]]:
    try:
        with open(LIKES_DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


def save_likes(likes: List[Tuple[int, int]]):
    with open(LIKES_DB_FILE, "wb") as f:
        pickle.dump(likes, f)


def like_comment_of_post(comment_id: int, user_id: int) -> bool:

    likes = load_comment_likes()  # or load_comment_likes() if you have that
    if (comment_id, user_id) in likes:
        return False

    comment = get_comment_by_id(comment_id)
    if not comment:
        return False

    likes.append((comment_id, user_id))
    save_likes(likes)
    increment_likes_count_of_comment(comment_id=comment_id)
    return True


def dislike_comment_of_post(comment_id: int, user_id: int) -> bool:

    likes = load_comment_likes()  # or load_comment_likes() if that's what you're using
    if (comment_id, user_id) not in likes:
        return False

    comment = get_comment_by_id(comment_id)
    if not comment:
        return False

    likes.remove((comment_id, user_id))
    save_likes(likes)
    decrement_likes_count_of_comment(comment_id=comment_id)
    return True



def get_likes_of_comment(comment_id: int) -> int:
    comments = load_comments()
    comment = next((c for c in comments if c.comment_id == comment_id), None)
    return comment.likes_nbr if comment else 0



def is_comment_liked_by_me(comment_id: int, user_id: int) -> bool:
    likes = load_comment_likes()
    return (comment_id, user_id) in likes


def increment_likes_count_of_comment(comment_id: int) -> bool:
    comments = load_comments()
    comment = next((c for c in comments if c.comment_id == comment_id), None)
    if not comment:
        return False
    comment.likes_nbr += 1
    save_comments(comments)
    return True


def decrement_likes_count_of_comment(comment_id: int) -> bool:
    comments = load_comments()
    comment = next((c for c in comments if c.comment_id == comment_id), None)
    if not comment:
        return False
    if comment.likes_nbr > 0:
        comment.likes_nbr -= 1
    save_comments(comments)
    return True


def get_comment_by_id(comment_id: int) -> CommentProfile | None:
    comments = load_comments()
    return next((c for c in comments if c.comment_id == comment_id), None)


def get_posts_count(user_id: int) -> int:
    """
    Returns the number of posts created by a given user.
    """
    posts = load_data_from_dat_file(POSTS_DB)
    user_posts = [p for p in posts if p.user_id == user_id]
    return len(user_posts)