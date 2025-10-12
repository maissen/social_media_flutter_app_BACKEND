from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from datetime import datetime
import os
import shutil
from src.schemas.generic_response import GenericResponse
from src.core.security import get_current_user_from_token
from src.crud.users_crud import update_user_profile_picture

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
        # Validate file type (only images)
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only image files are allowed."
            )

        # Create a unique filename
        filename = f"user_{current_user.user_id}_{int(datetime.utcnow().timestamp())}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Example: you might update the user's profile picture in DB here
        # update_user_profile_picture(current_user.id, filename)

        file_url = f"{UPLOAD_FILE_PREFIX}/{file_path}"  # if served by StaticFiles (e.g., app.mount("/static", StaticFiles(...)))

        update_user_profile_picture(file=file_url, user_id=current_user.user_id)

        return GenericResponse(
            success=True,
            data={"file_url": file_url},
            message="Profile picture updated successfully",
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        print(f"Error updating profile picture: {e}")
        return GenericResponse(
            success=False,
            data=None,
            message="Failed to upload profile picture",
            timestamp=datetime.utcnow()
        )
