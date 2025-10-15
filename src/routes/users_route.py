import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.core.security import get_current_user_from_token
from src.schemas.generic_response import GenericResponse
from src.crud.users_crud import get_user_by_id, update_user_bio, update_user_profile_picture, find_matching_username, check_following_status, follow, get_followers_of_user, get_followings_of_user, unfollow
from src.schemas.users import UpdateBioRequest, UserProfileSchema


router = APIRouter(prefix="", tags=["User Management"])
UPLOAD_DIR = "uploads/profile_pictures"
UPLOAD_FILE_PREFIX = os.getenv("UPLOAD_FILES_PREFIX")

@router.get("/profile/{user_id}", response_model=GenericResponse)
def get_user_profile(user_id: int, current_user=Depends(get_current_user_from_token)):
    """Get user profile by user ID. Requires a valid JWT token."""
    try:
        user = get_user_by_id(user_id)
        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=jsonable_encoder(GenericResponse(
                    success=False,
                    message="User not found",
                    timestamp=datetime.utcnow()
                ))
            )

        user_profile = UserProfileSchema(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            bio=user.bio,
            profile_picture=user.profile_picture,
            followers_count=len(get_followers_of_user(user_id=user_id)),
            following_count=len(get_followings_of_user(user_id=user_id)),
            posts_count=user.posts_count,
            created_at=user.created_at,
            is_following=check_following_status(user_1=current_user.user_id, user_2=user_id)
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data=user_profile,
                message="User profile retrieved successfully",
                timestamp=datetime.utcnow()
            ))
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                data=None,
                message="Failed",
                timestamp=datetime.utcnow()
            ))
        )


@router.put("/update/bio", response_model=GenericResponse)
def update_bio(
    payload: UpdateBioRequest,
    current_user=Depends(get_current_user_from_token)
):
    """Update user bio."""
    try:
        if not current_user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=jsonable_encoder(GenericResponse(
                    success=False,
                    data=None,
                    message="User not found",
                    timestamp=datetime.utcnow()
                ))
            )
        
        update_user_bio(user_id=current_user.user_id, payload=payload.new_bio)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data={"new_bio": payload.new_bio},
                message="Bio updated successfully",
                timestamp=datetime.utcnow()
            ))
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                data=None,
                message="Failed",
                timestamp=datetime.utcnow()
            ))
        )


@router.put("/update-profile-picture", response_model=GenericResponse, status_code=status.HTTP_200_OK)
async def update_profile_picture(
    file: UploadFile = File(..., description="Profile picture to upload"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Upload a new profile picture for the current user.
    """
    try:
        if not file.content_type.startswith("image/"):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder(GenericResponse(
                    success=False,
                    message="Invalid file type. Only image files are allowed.",
                    timestamp=datetime.utcnow()
                ))
            )

        filename = f"user_{current_user.user_id}_{int(datetime.utcnow().timestamp())}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = f"{UPLOAD_FILE_PREFIX}{file_path}"

        update_user_profile_picture(file=file_url, user_id=current_user.user_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data={"file_url": file_url},
                message="Profile picture updated successfully",
                timestamp=datetime.utcnow()
            ))
        )

    except Exception as e:
        print(f"Error updating profile picture: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                data=None,
                message="Failed to upload profile picture",
                timestamp=datetime.utcnow()
            ))
        )


    

@router.get("/search", response_model=GenericResponse)
def search_users(
    username: str = Query(..., min_length=1, description="Username to search for"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Search for users by username.
    Returns users whose username contains the search username (case-insensitive).
    """
    try:
        matching_users = find_matching_username(current_user=current_user.user_id, username=username)
        
        if not matching_users:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(GenericResponse(
                    success=True,
                    message="No users found",
                    timestamp=datetime.utcnow()
                ))
            )
        
        results = [
            UserProfileSchema(
                user_id=user.user_id,
                email=user.email,
                username=user.username,
                bio=user.bio,
                profile_picture=user.profile_picture,
                followers_count=user.followers_count,
                following_count=user.following_count,
                posts_count=user.posts_count,
                created_at=user.created_at,
                is_following=user.is_following
            ) for user in matching_users
        ]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data=results,
                message="Users retrieved successfully",
                timestamp=datetime.utcnow()
            ))
        )
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                data=None,
                message="Failed",
                timestamp=datetime.utcnow()
            ))
        )


@router.post("/follow-unfollow", response_model=GenericResponse)
def follow_unfollow(
    target_user_id: int,
    current_user=Depends(get_current_user_from_token)
):
    """
    Toggle following/unfollowing a target user.
    """
    try:
        if current_user.user_id == target_user_id:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder(GenericResponse(
                    success=False,
                    message="You cannot follow/unfollow yourself",
                    timestamp=datetime.utcnow()
                ))
            )

        if check_following_status(current_user.user_id, target_user_id):
            print(f"status : {check_following_status(current_user.user_id, target_user_id)}")
            success = unfollow(current_user.user_id, target_user_id)
            action = "unfollowed"
        else:
            success = follow(current_user.user_id, target_user_id)
            action = "followed"

        if not success:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(GenericResponse(
                    success=False,
                    message="Failed to update follow status",
                    timestamp=datetime.utcnow()
                ))
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data={
                    "is_following": check_following_status(current_user.user_id, target_user_id)
                },
                message=f"User {action} successfully",
                timestamp=datetime.utcnow()
            ))
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                data=None,
                message="An unexpected error occurred",
                timestamp=datetime.utcnow()
            ))
        )


@router.get("/followers", response_model=GenericResponse)
def get_followers(
    user_id: int = Query(..., description="ID of the user to get followers for"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Get all users who are following the given user.
    """
    try:
        followers_data = get_followers_of_user(user_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data=followers_data,
                message="Followers retrieved successfully",
                timestamp=datetime.utcnow()
            ))
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                data=None,
                message="An unexpected error occurred",
                timestamp=datetime.utcnow()
            ))
        )


@router.get("/followings", response_model=GenericResponse)
def get_followings(
    user_id: int = Query(..., description="ID of the user to get followings for"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Get all users that the given user is following.
    """
    try:
        followings_data = get_followings_of_user(user_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data=followings_data,
                message="Followings retrieved successfully",
                timestamp=datetime.utcnow()
            ))
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=jsonable_encoder(GenericResponse(
                success=False,
                data=None,
                message="Failed to fetch followings list",
                timestamp=datetime.utcnow()
            ))
        )
