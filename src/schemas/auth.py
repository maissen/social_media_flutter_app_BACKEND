from pydantic import BaseModel, EmailStr
from datetime import date


class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
