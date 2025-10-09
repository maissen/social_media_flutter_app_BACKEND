from fastapi import APIRouter, Depends, status
from datetime import datetime
from src.schemas.auth import RegisterUserRequest, LoginRequest
from src.schemas.generic_response import GenericResponse
from src.core.security import get_password_hash, verify_password, create_access_token
from src.services.auth_service import logout_user
from src.users_db import insert_user, get_user_by_email, get_new_user_id
from src.schemas.users import UserSchema

router = APIRouter(prefix="", tags=["Authentication"])



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

        # Create new user object
        user = UserSchema(
            user_id=get_new_user_id(),
            email=payload.email,
            username=payload.username,
            password=get_password_hash(payload.password),
            profile_picture="",
            bio="",
            date_of_birth=payload.date_of_birth,
            created_at=datetime.utcnow()
        )

        # add user to db
        insert_user(user=user)

        return GenericResponse(
            success=True,
            data=None,
            message="User registered successfully",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message="Oops, failed to register user",
            timestamp=datetime.utcnow()
        )


@router.post("/login", response_model=GenericResponse)
def login(payload: LoginRequest):
    try:
        user = get_user_by_email(payload.email)
        if not user or not hasattr(user, "password"):
            return GenericResponse(
                success=False,
                message="Failed, please submit a valid data",
                timestamp=datetime.utcnow()
            )

        if not verify_password(payload.password, user.password):
            return GenericResponse(
                success=False,
                message="Your password is wrong",
                timestamp=datetime.utcnow()
            )

        token = create_access_token(data={"sub": str(user.user_id)})
        expires_in = 36000  # 10 hours

        return GenericResponse(
            success=True,
            data={
                "access_token": token,
                "expires_in": expires_in,
                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                    "username": user.username,
                    "profile_picture": user.profile_picture
                }
            },
            message="Login successful",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message="An error occured",
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