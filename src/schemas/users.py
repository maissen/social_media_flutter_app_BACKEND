from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    user_id: int
    email: str
    username: str
    password: str
    created_at: datetime
    bio: Optional[str] = ""
    profile_picture: Optional[str] = ""
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    created_at: datetime
    is_following: bool = False


class UserProfileSchema(BaseModel):
    user_id: int
    email: str
    username: str
    bio: Optional[str] = ""
    profile_picture: Optional[str] = ""
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    created_at: datetime
    is_following: bool = False



class UpdateBioRequest(BaseModel):
    new_bio: str


class UpdateProfilePictureRequest(BaseModel):
    profile_picture: str


class UserProfileSimplified(BaseModel):
    user_id: int
    email: str
    username: str
    profile_picture: Optional[str] = ""
    is_following: bool = False
