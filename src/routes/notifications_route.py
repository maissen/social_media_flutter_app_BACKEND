from typing import List
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from schemas.notification import NotificationSchema
from src.schemas.generic_response import GenericResponse
from src.crud.notifications_crud import get_notifs_of_user, mark_notification_as_read

router = APIRouter()

@router.get("", response_model=GenericResponse)
def get_notifications(user_id: int = Query(..., description="ID of the user to fetch notifications for")):
    """
    Retrieve all notifications for a specific user.
    """
    try:
        notifications = get_notifs_of_user(user_id)

        # Sort notifications by created_at descending (newest first)
        notifications_sorted = sorted(notifications, key=lambda x: x.created_at, reverse=True)

        for notif in notifications_sorted:
            mark_notification_as_read(notif.id)



        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(GenericResponse(
                success=True,
                data=notifications_sorted,
                message=f"{len(notifications)} notifications found",
                timestamp=datetime.utcnow()
            ))
        )

    except Exception as e:
        print(f"Error retrieving notifications for user {user_id}: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(GenericResponse(
                success=False,
                data=None,
                message="Failed to retrieve notifications",
                timestamp=datetime.utcnow()
            ))
        )


@router.get("/new/{user_id}", response_model=List[NotificationSchema])
def get_new_notifications(user_id: int):

    notifications = get_notifs_of_user(user_id)
    unread_notifications = [notif for notif in notifications if not notif.is_read]

    notifications_sorted = sorted(unread_notifications, key=lambda x: x.created_at, reverse=True)


    for notif in unread_notifications:
        mark_notification_as_read(notif.id)

    return notifications_sorted
