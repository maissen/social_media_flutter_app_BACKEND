from fastapi import APIRouter, Depends
from datetime import datetime
from src.schemas.generic_response import GenericResponse
from src.users_db import get_user_by_id

router = APIRouter(prefix="", tags=["User Management"])


@router.get("/profile/{user_id}", response_model=GenericResponse)
def get_user_profile(user_id: int):
    """Get user profile by user ID."""
    try:
        # Find the user by ID
        user = get_user_by_id(user_id)
        
        if not user:
            return GenericResponse(
                success=False,
                data=None,
                message="User not found",
                timestamp=datetime.utcnow()
            )
        
        # Check if current user is following this user
        # Since we don't have a followers system yet, we'll set this to False
        is_following = False
        
        # Count followers, following, and posts
        # Since we don't have these systems yet, we'll set them to 0
        followers_count = 0
        following_count = 0
        posts_count = 0
        
        return GenericResponse(
            success=True,
            data={
                "user_id": user.user_id,
                "email": user.email,
                "username": user.username,
                "bio": user.bio,
                "profile_picture": user.profile_picture,
                "followers_count": followers_count,
                "following_count": following_count,
                "posts_count": posts_count,
                "created_at": user.created_at.isoformat() + "Z",
                "is_following": is_following
            },
            message="User profile retrieved successfully",
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            data=None,
            message="Failed",
            timestamp=datetime.utcnow()
        )