import re
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from datetime import datetime
import os
import shutil

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.crud.notifications_crud import create_new_notification
from src.schemas.generic_response import GenericResponse
from src.core.security import get_current_user_from_token
from src.crud.users_crud import get_followers_of_user, update_user_profile_picture
# from src.routes.ws import broadcast_to_followers_of_user

router = APIRouter(prefix="", tags=["Profile Management"])

UPLOAD_DIR = "uploads/profile_pictures"
UPLOAD_FILE_PREFIX = "url"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/update-profile-picture", response_model=GenericResponse, status_code=status.HTTP_200_OK)
async def update_profile_picture(
    file: UploadFile = File(..., description="Profile picture to upload"),
    current_user=Depends(get_current_user_from_token)
):
    """
    Upload a new profile picture for the current user.
    The image file is saved to the server in `static/uploads/profile_pictures/`.
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

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_ext = os.path.splitext(file.filename)[1]

        # Remove spaces and other unsafe characters from the original filename
        clean_name = re.sub(r"[^A-Za-z0-9_-]", "", os.path.splitext(file.filename)[0])

        timestamp = int(datetime.utcnow().timestamp())
        filename = f"user_{timestamp}_{clean_name}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = f"{UPLOAD_FILE_PREFIX}/{filename}"

        update_user_profile_picture(file=file_url, user_id=current_user.user_id)

        
        my_followers = get_followers_of_user(current_user.username)

        if my_followers is not None or len(my_followers) > 0:
            for follower in my_followers:
                notif = create_new_notification(
                    user_id=follower.user_id,
                    actor_id=current_user.user_id,
                    type="update profile picture",
                    message=f"{current_user.username} updated his profile picture"
                )

        broadcast_to_followers_of_user(followers=my_followers, notification=notif)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data={"profile_picture_url": file_url},
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