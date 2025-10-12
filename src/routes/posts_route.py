import os
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Form, File, Query, UploadFile, status
from src.crud.posts_and_comments_crud import add_comment_to_post, remove_comment_from_post, dislike_comment_of_post, get_comment_by_id, get_comments_of_post, is_comment_liked_by_me, like_comment_of_post
from src.crud.posts_and_comments_crud import delete_a_post, dislike_post, get_post_by_id, get_posts_of_user, create_new_post, get_posts_count, is_post_liked_by_me, like_post, update_a_post
from src.schemas.generic_response import GenericResponse
from src.schemas.posts import CommentProfile, CreateOrUpdateCommentSchema, PostSchema, UpdatePostSchema
from src.core.security import get_current_user_from_token


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

        create_new_post(new_post)

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
    post = get_post_by_id(post_id)
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



@router.delete("/delete", response_model=GenericResponse)
def delete_post(
    post_id: int = Query(..., description="ID of the post to delete"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Delete a post by its ID.
    Only the post owner can delete their post.
    """
    try:
        post = get_post_by_id(post_id)
        if not post:
            return GenericResponse(
                success=False,
                message="Post not found",
                timestamp=datetime.utcnow()
            )

        if post.user_id != current_user.user_id:
            return GenericResponse(
                success=False,
                message="You are not allowed to delete this post",
                timestamp=datetime.utcnow()
            )

        success = delete_a_post(post_id)
        if success:
            return GenericResponse(
                success=True,
                message="Post deleted successfully",
                timestamp=datetime.utcnow()
            )
        else:
            return GenericResponse(
                success=False,
                message="Failed to delete post",
                timestamp=datetime.utcnow()
            )

    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message="An unexpected error occurred",
            timestamp=datetime.utcnow()
        )
    


@router.post("/like-deslike/{post_id}", response_model=GenericResponse)
def like_or_dislike_post(
    post_id: int,
    current_user=Depends(get_current_user_from_token)
):
    """
    Like or dislike a post.
    - If already liked → dislike.
    - If not liked → like.
    """
    try:
        post = get_post_by_id(post_id)
        if not post:
            return GenericResponse(
                success=False,
                message="Post not found",
                timestamp=datetime.utcnow()
            )

        user_id = current_user.user_id

        if is_post_liked_by_me(user_id, post_id):
            # Already liked → remove like
            success = dislike_post(user_id, post_id)
            is_liked = False
        else:
            # Not liked → add like
            success = like_post(user_id, post_id)
            is_liked = True

        if not success:
            return GenericResponse(
                success=False,
                message="Failed to like/dislike post",
                timestamp=datetime.utcnow()
            )
    
        if is_liked:
            return GenericResponse(
                success=True,
                data={"is_liked": is_liked},
                message="Post is liked successfully",
                timestamp=datetime.utcnow()
            )
        else:
            return GenericResponse(
                success=True,
                data={"is_liked": is_liked},
                message="Post is desliked successfully",
                timestamp=datetime.utcnow()
            )

    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            message="Failed",
            timestamp=datetime.utcnow()
        )
    


@router.post("/comments/create", response_model=GenericResponse, status_code=status.HTTP_201_CREATED)
def create_new_comment(
    content: CreateOrUpdateCommentSchema,
    post_id: int = Query(..., description="ID of the post to comment on"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Create a new comment on a post.
    The post_id is provided as a query parameter.
    """
    try:
        comment = add_comment_to_post(current_user, post_id, content.content)

        return GenericResponse(
            success=True,
            data=comment.dict(),
            message="Comment created successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(f"Error creating comment: {e}")
        return GenericResponse(
            success=False,
            data=None,
            message="Failed to create comment",
            timestamp=datetime.utcnow()
        )
    

@router.delete("/comments/delete", response_model=GenericResponse, status_code=status.HTTP_200_OK)
def delete_comment(
    comment_id: int = Query(..., description="ID of the comment to delete"),
    post_id: int = Query(..., description="ID of the post the comment belongs to"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Delete a specific comment of a post.
    Only the comment owner or an admin should be allowed to delete (if implemented).
    """
    try:
        success = remove_comment_from_post(comment_id, post_id)

        if not success:
            return GenericResponse(
                success=False,
                message="Comment not found or could not be deleted",
                timestamp=datetime.utcnow()
            )

        return GenericResponse(
            success=True,
            message="Comment deleted successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(f"Error deleting comment: {e}")
        return GenericResponse(
            success=False,
            message="An unexpected error occurred while deleting the comment",
            timestamp=datetime.utcnow()
        )
    

@router.post("/comments/like-dislike", response_model=GenericResponse)
def toggle_like_comment(
    comment_id: int = Query(..., description="ID of the comment to like/unlike"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Like a comment if not liked; otherwise, remove like (dislike).
    """

    try:
        comment = get_comment_by_id(comment_id=comment_id)

        if not comment:
            return GenericResponse(
                success=False,
                message="Comment is not found",
                timestamp=datetime.utcnow()
            )
    except:
        return GenericResponse(
            success=False,
            message="An error occured while looking for the comment",
            timestamp=datetime.utcnow()
        )

    try:
        user_id = current_user.user_id
        already_liked = is_comment_liked_by_me(comment_id, user_id)

        if already_liked:
            # User already liked → remove like
            success = dislike_comment_of_post(comment_id, user_id)
            action = "disliked"
        else:
            # User has not liked → add like
            success = like_comment_of_post(comment_id, user_id)
            action = "liked"

        if not success:
            return GenericResponse(
                success=False,
                message="Failed to like/dislike comment",
                timestamp=datetime.utcnow()
            )

        return GenericResponse(
            success=True,
            data={
                "is_liked": is_comment_liked_by_me(comment_id=comment_id, user_id=current_user.user_id),
                "likes_nbr": comment.likes_nbr
            },
            message=f"Comment {action} successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            data=None,
            message="An unexpected error occurred",
            timestamp=datetime.utcnow()
        )
    

@router.get("/comments/all", response_model=GenericResponse)
def get_comments(
    post_id: int = Query(..., description="ID of the post to retrieve comments for"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Get all comments of a given post as CommentProfile objects.
    Does not include likes or is_liked_by_me.
    """
    try:
        comments: List[CommentProfile] = get_comments_of_post(post_id)

        return GenericResponse(
            success=True,
            data=comments,
            message="Comments retrieved successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(e)
        return GenericResponse(
            success=False,
            data=[],
            message="Failed to retrieve comments",
            timestamp=datetime.utcnow()
        )