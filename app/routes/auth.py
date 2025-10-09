from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.auth import RegisterUserRequest, LoginRequest, GenericResponse
from app.database import get_db
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.auth_service import logout_user

router = APIRouter(prefix="", tags=["Authentication"])


@router.post("/register", response_model=GenericResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterUserRequest, db: Session = Depends(get_db)):

    try:
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            return GenericResponse(
                success=False,
                data=None,
                message="Email already exists",
                timestamp=datetime.utcnow()
            )

        user = User(
            email=payload.email,
            username=payload.username,
            hashed_password=get_password_hash(payload.password),
            date_of_birth=payload.date_of_birth
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return GenericResponse(
            success=True,
            data=None,
            message="User registered successfully",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        db.rollback()
        print(f"e")
        return GenericResponse(
            success=False,
            message=f"Oops, failed to register user",
            timestamp=datetime.utcnow()
        )


@router.post("/login", response_model=GenericResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):

    #! """Authenticate and return access token."""

    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            return GenericResponse(
                success=False,
                message=f"Failed, please submit a valid data",
                timestamp=datetime.utcnow()
            )
        
        if not verify_password(payload.password, user.hashed_password):
            return GenericResponse(
                success=False,
                message=f"Your password is wrong",
                timestamp=datetime.utcnow()
            )

        token = create_access_token(data={"sub": str(user.id)})
        expires_in = 36000  # 10 hour

        return GenericResponse(
            success=True,
            data={
                "access_token": token,
                "expires_in": expires_in,
                "user": {
                    "user_id": str(user.id),
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
        return GenericResponse(
            success=False,
            message=f"Failed: {str(e)}",
            timestamp=datetime.utcnow()
        )
