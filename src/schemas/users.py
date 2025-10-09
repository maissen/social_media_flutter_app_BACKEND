from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    user_id: int
    email: str
    username: str
    password: str
    bio: Optional[str] = ""
    profile_picture: Optional[str] = ""
    date_of_birth: date
    created_at: datetime

    class Config:
        orm_mode = True
