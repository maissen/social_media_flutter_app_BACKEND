from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.schemas.generic_response import GenericResponse
from src.core.security import get_current_user  # JWT auth dependency
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile/{user_id}", response_model=GenericResponse)
def get_user_profile(
    user_id: str,
    current_user: User = Depends(get_current_user),  # ensures JWT is valid
    db: Session = Depends(get_db),
):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return GenericResponse(
                success=False,
                data=None,
                message="User not found",
                timestamp=datetime.utcnow()
            )

        # Count followers, following, and posts
        followers_count = db.query(User).filter(User.following.any(id=user.id)).count()
        following_count = len(user.following)  # Assuming relationship defined
        posts_count = db.query(user.posts.__class__).filter_by(user_id=user.id).count()

        is_following = current_user.id in [f.id for f in user.followers]

        data = {
            "user_id": str(user.id),
            "email": user.email,
            "username": user.username,
            "bio": user.bio,
            "profile_picture": user.profile_picture,
            "followers_count": followers_count,
            "following_count": following_count,
            "posts_count": posts_count,
            "created_at": user.created_at.isoformat(),
            "is_following": is_following
        }

        return GenericResponse(
            success=True,
            data=data,
            message="User profile retrieved successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message="Failed",
            timestamp=datetime.utcnow()
        )
