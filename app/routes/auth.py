from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.auth import RegisterUserRequest, LoginRequest, AuthResponse, GenericResponse
from app.database import get_db
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.auth_service import logout_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=GenericResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterUserRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

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
        return GenericResponse(
            success=False,
            message=f"Failed: {str(e)}",
            timestamp=datetime.utcnow()
        )


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate and return access token."""
    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token(data={"sub": str(user.id)})
        expires_in = 3600  # 1 hour

        return AuthResponse(
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
        return AuthResponse(
            success=False,
            message=f"Failed: {str(e)}",
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
