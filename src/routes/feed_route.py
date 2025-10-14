from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from src.crud.posts_and_comments_crud import load_feed_of_user, load_recent_posts
from src.crud.users_crud import get_simplified_user_obj_by_id
from src.schemas.generic_response import GenericResponse
from src.core.security import get_current_user_from_token

router = APIRouter(prefix="", tags=["Profile Management"])


@router.get("", response_model=GenericResponse, status_code=status.HTTP_200_OK)
async def get_user_feed(current_user=Depends(get_current_user_from_token)):
    try:
        feed = load_feed_of_user(user_id=current_user.user_id)

        for item in feed:
            post_owner = get_simplified_user_obj_by_id(user_id=item.user_id)

            if post_owner is not None:
                item.user = post_owner

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data=feed,
                message="Feed is fetched successfully",
                timestamp=datetime.utcnow()
            ))
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                message="An error occurred while loading your feed",
                timestamp=datetime.utcnow()
            ))
        )


@router.get("/explore", response_model=GenericResponse, status_code=status.HTTP_200_OK)
async def get_explore_feed(
    current_user=Depends(get_current_user_from_token)
):
    """
    Get the most recent posts from all users (Explore feed), excluding the current user's posts.
    """
    try:
        posts = load_recent_posts()

        # Exclude current user's posts
        posts = [post for post in posts if post.user_id != current_user.user_id]

        #? attach user object with each post
        for item in posts:
            post_owner = get_simplified_user_obj_by_id(user_id=item.user_id)
            if post_owner is not None:
                item.user = post_owner

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data=posts,
                message="Explore feed loaded successfully",
                timestamp=datetime.utcnow()
            ))
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                message="An error occurred while loading the explore feed",
                timestamp=datetime.utcnow()
            ))
        )
