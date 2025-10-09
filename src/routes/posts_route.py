import os
from datetime import datetime
from fastapi import APIRouter, Depends, Form, File, UploadFile, status
from src.posts_crud import get_a_single_post, get_posts_of_user, insert_new_post, get_posts_count, update_a_post
from src.schemas.generic_response import GenericResponse
from src.schemas.posts import PostSchema, UpdatePostSchema
from src.core.security import get_current_user_from_token
from src.users_crud import increment_posts_count_of_user, decrement_posts_count_of_user

# Directory where uploaded media will be stored
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Prefix for filenames
UPLOAD_FILES_PREFIX = os.getenv("UPLOAD_FILES_PREFIX")

router = APIRouter(prefix="", tags=["Posts"])


@router.post(
    "/create",
    response_model=GenericResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_post(
    content: str = Form("", description="Text content of the post"),
    media_file: UploadFile = File(None, description="Optional media file to upload"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Create a new post for the logged-in user.
    Accepts optional media uploads (image/video).
    """
    try:
        if content.strip() == "" and media_file is None:
            return GenericResponse(
                success=False,
                message="Please add content or a media file to your post.",
                timestamp=datetime.utcnow()
            )

        # Determine post_id before saving file
        post_id = get_posts_count() + 1

        media_url = ""
        if media_file:
            file_ext = os.path.splitext(media_file.filename)[1]
            file_name = f"post_{post_id}{file_ext}"
            file_path = os.path.join(UPLOAD_DIR, file_name)

            with open(file_path, "wb") as buffer:
                buffer.write(await media_file.read())

            # URL or relative path for access
            media_url = f"{UPLOAD_FILES_PREFIX}/{UPLOAD_DIR}{file_name}"

        new_post = PostSchema(
            post_id=post_id,
            user_id=current_user.user_id,
            content=content,
            media_url=media_url,
            created_at=datetime.utcnow(),
            likes_nbr=0,
            comments_nbr=0,
            is_liked_by_me=False
        )

        insert_new_post(new_post)
        increment_posts_count_of_user(current_user.user_id)

        return GenericResponse(
            success=True,
            data=new_post,
            message="Post created successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print("Error creating post:", e)
        return GenericResponse(
            success=False,
            data=None,
            message="Failed to create post",
            timestamp=datetime.utcnow()
        )



@router.get("/{user_id}", response_model=GenericResponse)
def get_user_posts(user_id: int, current_user=Depends(get_current_user_from_token)):
    """
    Retrieve all posts for a specific user.
    Requires a valid JWT token.
    """
    try:
        posts = get_posts_of_user(current_user_id=current_user.user_id, target_user_id=user_id)
        return GenericResponse(
            success=True,
            data=posts,
            message=f"posts received successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            data=None,
            message="Failed to retrieve posts",
            timestamp=datetime.utcnow()
        )
    


@router.put("/update/{post_id}", response_model=GenericResponse)
def update_post(
    post_id: int,
    payload: UpdatePostSchema,
    current_user=Depends(get_current_user_from_token)
):
    """
    Update the content of a post.
    Only the user who created the post can update it.
    """
    post = get_a_single_post(post_id)
    if not post:
        return GenericResponse(
            success=False,
            message="couldn't find post",
            timestamp=datetime.utcnow()
        )

    if post.user_id != current_user.user_id:
        return GenericResponse(
            success=False,
            message="You need to be the owner of the post in order to update it",
            timestamp=datetime.utcnow()
        )
    
    if payload.new_content == "": 
        return GenericResponse(
            success=False,
            message="Please provide the new text to update post",
            timestamp=datetime.utcnow()
        )

    updated_post = update_a_post(post_id, payload.new_content)
    if not updated_post:
        return GenericResponse(
            success=False,
            message="Failed to update post",
            timestamp=datetime.utcnow()
        )

    return GenericResponse(
        success=True,
        data=updated_post,
        message="Post updated successfully",
        timestamp=datetime.utcnow()
    )