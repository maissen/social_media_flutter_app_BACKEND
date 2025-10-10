from fastapi import APIRouter, Depends, status, Query
from datetime import datetime
from src.posts_crud import load_feed_of_user, load_recent_posts
from src.schemas.generic_response import GenericResponse
from src.core.security import get_current_user_from_token
from src.users_crud import get_user_by_id

router = APIRouter(prefix="", tags=["Profile Management"])


@router.get("", response_model=GenericResponse, status_code=status.HTTP_200_OK)
async def get_user_feed(
    current_user=Depends(get_current_user_from_token)
):
    
    try:

        feed = load_feed_of_user(user_id=current_user.user_id)
        print(f"feed length {len(feed)}")

        return GenericResponse(
            success=True,
            data=feed,
            message=f"Feed is fetched successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message=f"An error occured while loading your feed",
            timestamp=datetime.utcnow()
        )
    


@router.get("/explore", response_model=GenericResponse, status_code=status.HTTP_200_OK)
async def get_explore_feed(
    limit: int = 20,
    current_user=Depends(get_current_user_from_token)
):
    """
    Get the most recent posts from all users (Explore feed).
    """
    try:
        posts = load_recent_posts(limit=limit)
        return GenericResponse(
            success=True,
            data=posts,
            message="Explore feed loaded successfully",
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message="An error occurred while loading the explore feed",
            timestamp=datetime.utcnow()
        )