from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class CommentProfile(BaseModel):
    comment_id: int
    user_id: int
    username: str
    profile_picture: Optional[str] = ""
    comment_payload: str
    created_at: datetime

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    post_id: int
    user_id: int
    content: str
    media_url: Optional[str] = ""
    created_at: datetime
    likes_nbr: int = 0
    comments_nbr: int = 0
    is_liked_by_me: bool = False

    class Config:
        orm_mode = True


class UpdatePostSchema(BaseModel):
    new_content: str
