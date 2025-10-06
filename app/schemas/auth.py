from pydantic import BaseModel, EmailStr, constr
from datetime import datetime, date
from typing import Optional, Any, Dict

class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: constr(min_length=8, max_length=72)  # enforce bcrypt safe length
    date_of_birth: date


class LoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=72)


class GenericResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: str
    timestamp: datetime


class AuthResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str
    timestamp: datetime
