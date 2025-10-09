from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import List, Optional
from src.schemas.auth import RegisterUserRequest, LoginRequest
from src.schemas.generic_response import GenericResponse
from src.models.user import User
from src.core.security import get_password_hash, verify_password, create_access_token
from src.services.auth_service import logout_user
import uuid

router = APIRouter(prefix="", tags=["Authentication"])

# In-memory user storage
users_db: List[dict] = []


def get_user_by_email(email: str) -> Optional[dict]:
    """Find user by email in the in-memory list."""
    return next((user for user in users_db if user["email"] == email), None)


def get_user_by_id(user_id: str) -> Optional[dict]:
    """Find user by ID in the in-memory list."""
    return next((user for user in users_db if user["id"] == user_id), None)


@router.post("/register", response_model=GenericResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterUserRequest):
    try:
        existing_user = get_user_by_email(payload.email)
        if existing_user:
            return GenericResponse(
                success=False,
                data=None,
                message="Email already exists",
                timestamp=datetime.utcnow()
            )

        # Create new user dictionary
        user = {
            "id": str(uuid.uuid4()),
            "email": payload.email,
            "username": payload.username,
            "hashed_password": get_password_hash(payload.password),
            "date_of_birth": payload.date_of_birth,
            "profile_picture": None,
            "created_at": datetime.utcnow()
        }

        users_db.append(user)

        return GenericResponse(
            success=True,
            data=None,
            message="User registered successfully",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        print(f"{e}")
        return GenericResponse(
            success=False,
            message=f"Oops, failed to register user",
            timestamp=datetime.utcnow()
        )


@router.post("/login", response_model=GenericResponse)
def login(payload: LoginRequest):
    try:
        user = get_user_by_email(payload.email)
        if not user:
            return GenericResponse(
                success=False,
                message=f"Failed, please submit a valid data",
                timestamp=datetime.utcnow()
            )
        
        if not verify_password(payload.password, user["hashed_password"]):
            return GenericResponse(
                success=False,
                message=f"Your password is wrong",
                timestamp=datetime.utcnow()
            )

        token = create_access_token(data={"sub": user["id"]})
        expires_in = 36000  # 10 hour

        return GenericResponse(
            success=True,
            data={
                "access_token": token,
                "expires_in": expires_in,
                "user": {
                    "user_id": user["id"],
                    "email": user["email"],
                    "username": user["username"],
                    "profile_picture": user.get("profile_picture")
                }
            },
            message="Login successful",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message=f"An error occured",
            timestamp=datetime.utcnow()
        )


@router.post("/logout", response_model=GenericResponse)
def logout(token: str = Depends(logout_user)):
    """Logout user by invalidating the token."""
    
    try:
        return GenericResponse(
            success=True,
            data=None,
            message="Logged out successfully",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message=f"Failed to logout",
            timestamp=datetime.utcnow()
        )