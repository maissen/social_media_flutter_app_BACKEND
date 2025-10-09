from datetime import datetime
from pydantic import BaseModel

class CreatePostSchema(BaseModel):
    user_id: int
    content: str
    media_url: str
    created_at: datetime