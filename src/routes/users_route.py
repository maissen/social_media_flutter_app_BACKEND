from typing import List
from fastapi import APIRouter, Depends, Query
from datetime import datetime
from src.core.security import get_current_user_from_token
from src.schemas.generic_response import GenericResponse
from src.users_crud import get_user_by_id, update_user_bio, update_user_profile_picture, find_matching_username
from src.schemas.users import UpdateProfilePictureRequest, UpdateBioRequest, UserProfileSchema, UserSearchedSchema
from src.followers_crud import check_following_status, follow, get_followers_of_user, get_followings_of_user, load_followers, unfollow


router = APIRouter(prefix="", tags=["User Management"])


@router.get("/profile/{user_id}", response_model=GenericResponse)
def get_user_profile(user_id: int, current_user=Depends(get_current_user_from_token)):
    """Get user profile by user ID. Requires a valid JWT token."""
    try:
        # The logged-in user is `current_user`
        user = get_user_by_id(user_id)
        
        if not user:
            return GenericResponse(
                success=False,
                message="User not found",
                timestamp=datetime.utcnow()
            )

        # Convert UserSchema to UserProfileSchema
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
            is_following=user.is_following
        )

        return GenericResponse(
            success=True,
            data=user_profile,
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

@router.put("/update/bio", response_model=GenericResponse)
def update_user_bio(
    payload: UpdateBioRequest,
    current_user=Depends(get_current_user_from_token)
):
    
    """Update user bio."""
    try:
        if not current_user:
            return GenericResponse(
                success=False,
                data=None,
                message="User not found",
                timestamp=datetime.utcnow()
            )
        
        # Update the bio
        update_user_bio(user_id=current_user.user_id, payload=payload.new_bio)
        
        return GenericResponse(
            success=True,
            data={
                "new_bio": payload.new_bio
            },
            message="Bio updated successfully",
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


@router.put("/update/profile-picture", response_model=GenericResponse)
def update_profile_picture(
    payload: UpdateProfilePictureRequest, 
    current_user=Depends(get_current_user_from_token)
):
    """Update user profile picture."""
    try:
        
        if not current_user:
            return GenericResponse(
                success=False,
                data=None,
                message="User not found",
                timestamp=datetime.utcnow()
            )
        
        # Update the profile picture
        print("current user " + str(current_user.user_id))
        current_user.profile_picture = payload.profile_picture

        update_user_profile_picture(
            user_id=current_user.user_id,
            payload=UpdateProfilePictureRequest(profile_picture=current_user.profile_picture)
        )
        return GenericResponse(
            success=True,
            data={
                "profile_picture": current_user.profile_picture
            },
            message="Profile picture updated successfully",
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
        # Search for users with matching username (case-insensitive)
        matching_users = find_matching_username(username=username)
        
        if not matching_users or matching_users == []:
            return GenericResponse(
                success=True,
                message="No users found",
                timestamp=datetime.utcnow()
            )
        
        # Format the results
        results = []
        for user in matching_users:
            results.append(get_user_by_id(user.user_id))
        
        # Convert to schema
        results = [UserSearchedSchema(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            profile_picture=user.profile_picture
        ) for user in matching_users]
        
        return GenericResponse(
            success=True,
            data=results,
            message="Users retrieved successfully",
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
    

@router.post("/follow-unfollow", response_model=GenericResponse)
def follow_unfollow(
    target_user_id: int,  # Query parameter
    current_user=Depends(get_current_user_from_token)
):
    """
    Toggle following/unfollowing a target user.
    If already following, it will unfollow; otherwise, it will follow.
    """
    try:
        if current_user.user_id == target_user_id:
            return GenericResponse(
                success=False,
                message="You cannot follow/unfollow yourself",
                timestamp=datetime.utcnow()
            )

        if check_following_status(current_user.user_id, target_user_id):
            # Already following → unfollow
            success = unfollow(current_user.user_id, target_user_id)
            action = "unfollowed"
        else:
            # Not following → follow
            success = follow(current_user.user_id, target_user_id)
            action = "followed"

        if not success:
            return GenericResponse(
                success=False,
                message="Failed to update follow status",
                timestamp=datetime.utcnow()
            )

        return GenericResponse(
            success=True,
            data={
                "is_following": check_following_status(current_user.user_id, target_user_id)
            },
            message=f"User {action} successfully",
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
    

@router.get("/followers", response_model=GenericResponse)
def get_followers(
    user_id: int = Query(..., description="ID of the user to get followers for"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Get all users who are following the given user.
    Requires a valid JWT token.
    """
    try:
        followers_data: List = get_followers_of_user(user_id)

        return GenericResponse(
            success=True,
            data=followers_data,
            message="Followers retrieved successfully",
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
    

@router.get("/followings", response_model=GenericResponse)
def get_followings(
    user_id: int = Query(..., description="ID of the user to get followings for"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Get all users that the given user is following.
    Requires a valid JWT token.
    """
    try:
        followings: List = get_followings_of_user(user_id)

        return GenericResponse(
            success=True,
            data=followings,
            message="Followings retrieved successfully",
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
