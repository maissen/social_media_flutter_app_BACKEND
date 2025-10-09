from fastapi import APIRouter, Depends, Query
from datetime import datetime
from src.core.security import get_current_user_from_token
from src.schemas.generic_response import GenericResponse
from src.users_db import get_user_by_id, update_user_bio, update_user_profile_picture
from src.schemas.users import UpdateProfilePictureRequest, UpdateBioRequest, UserProfileSchema, UserSearchedSchema

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
            followers_count=user.followers_count,
            following_count=user.following_count,
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
    

# @router.get("/search", response_model=GenericResponse)
# def search_users(
#     username: str = Query(..., min_length=1, description="Username to search for"),
# ):
#     """
#     Search for users by username.
#     Returns users whose username contains the search query (case-insensitive).
#     """
#     try:
#         # Search for users with matching username (case-insensitive)
#         matching_users = [
#             user for user in users_db
#             if username.lower() in user.username.lower()
#         ]
        
#         # Format the results
#         results = []
#         for user in matching_users:
#             results.append(get_user_by_id(user.user_id))

#         if not matching_users:
#             return GenericResponse(
#                 success=True,
#                 message="No users found",
#                 timestamp=datetime.utcnow()
#             )
        
#         # Convert to schema
#         results = [UserSearchedSchema(
#             user_id=user.user_id,
#             email=user.email,
#             username=user.username,
#             profile_picture=user.profile_picture
#         ) for user in matching_users]
        
#         return GenericResponse(
#             success=True,
#             data=results,
#             message="Users retrieved successfully",
#             timestamp=datetime.utcnow()
#         )
    
#     except Exception as e:
#         print(e)
#         return GenericResponse(
#             success=False,
#             data=None,
#             message="Failed",
#             timestamp=datetime.utcnow()
#         )