from datetime import datetime
from pydantic import BaseModel
from typing import Any

class PostSchema(BaseModel):
    user_id: int
    content: str
    media_url: str
    created_at: datetime
    likes_nbr: int = 0
    comments_nbr: int = 0
    comments_list: list[Any] = []


