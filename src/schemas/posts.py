from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from src.schemas.users import UserProfileSimplified

class CommentProfile(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    user: Optional[UserProfileSimplified] = None
    username: str
    profile_picture: Optional[str] = ""
    comment_payload: str
    created_at: datetime
    likes_nbr: int = 0
    is_liked_by_me: bool = False



class PostSchema(BaseModel):
    post_id: int
    user_id: int
    user: Optional[UserProfileSimplified] = None
    content: str
    media_url: str
    created_at: datetime
    likes_nbr: int = 0
    comments_nbr: int = 0
    is_liked_by_me: bool = False


class UpdatePostSchema(BaseModel):
    new_content: str


class CreateOrUpdateCommentSchema(BaseModel):
    content: str