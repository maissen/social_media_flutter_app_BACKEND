from datetime import datetime
from fastapi import APIRouter, Depends, Form, status
from src.posts_crud import insert_new_post, get_posts_count, get_comments_count, get_likes_count
from src.schemas.generic_response import GenericResponse
from src.schemas.posts import PostSchema
from src.core.security import get_current_user_from_token

router = APIRouter(prefix="", tags=["Authentication"])

@router.post("/create", 
    response_model=GenericResponse, 
    status_code=status.HTTP_201_CREATED
)
def create_post(
    content: str = Form(..., description="Text content of the post"),
    media_url: str = Form("", description="Optional media URL for the post"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Create a new post for the logged-in user.
    Requires a valid JWT token.
    """
    try:

        if content == "" and media_url == "":
            return GenericResponse(
                success=False,
                message="Please add content to your post",
                timestamp=datetime.utcnow()
            )

        new_post = PostSchema(
            post_id=get_posts_count()+1,
            user_id=current_user.user_id,
            content=content,
            media_url=media_url,
            created_at=datetime.utcnow(),
            likes_nbr=0,
            comments_nbr=0
        )

        insert_new_post(new_post)

        return GenericResponse(
            success=True,
            data=None,
            message="Post created successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print("Error creating post:", e)
        return GenericResponse(
            success=False,
            data=None,
            message="Failed to create  post",
            timestamp=datetime.utcnow()
        )