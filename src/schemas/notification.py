from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class NotificationSchema(BaseModel):
    id: int
    user_id: int
    actor_id: int
    type: str
    post_id: int
    comment_id: Optional[int] = None
    message: str
    is_read: bool
    created_at: datetime
