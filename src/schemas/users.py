from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    user_id: int
    email: str
    username: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    date_of_birth: date
    created_at: datetime

    class Config:
        orm_mode = True
