from pydantic import BaseModel, EmailStr
from datetime import date


class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    date_of_birth: date


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
