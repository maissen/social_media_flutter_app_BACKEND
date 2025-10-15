import pickle
from typing import List, Optional
from datetime import datetime
from src.schemas.notification import NotificationSchema

NOTIFICATIONS_DB_FILE = "database/notifications_database.dat"

# ======================
# Notifications CRUD
# ======================

def load_notifications() -> List[NotificationSchema]:
    """Load notifications from the file."""
    try:
        with open(NOTIFICATIONS_DB_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def save_notifications(notifications: List[NotificationSchema]):
    """Save notifications to the file."""
    with open(NOTIFICATIONS_DB_FILE, "wb") as f:
        pickle.dump(notifications, f)

def generate_new_notification_id() -> int:
    """Generate a new notification ID."""
    notifications = load_notifications()
    return len(notifications) + 1

def create_new_notification(user_id: int, actor_id: int, type: str, post_id: Optional[int] = None,
                            comment_id: Optional[int] = None, message: Optional[str] = None) -> NotificationSchema:
    """Create and save a new notification."""
    notifications = load_notifications()

    new_notif = NotificationSchema(
        id=generate_new_notification_id(),
        user_id=user_id,
        actor_id=actor_id,
        type=type,
        post_id=post_id,
        comment_id=comment_id,
        message=message or "",
        is_read=False,
        created_at=datetime.now()
    )

    notifications.append(new_notif)
    save_notifications(notifications)
    return new_notif

def get_notifs_of_user(user_id: int) -> List[NotificationSchema]:
    """Retrieve all notifications for a given user, sorted by newest first."""
    notifications = load_notifications()
    user_notifications = [notif for notif in notifications if notif.user_id == user_id]
    return sorted(user_notifications, key=lambda x: x.created_at, reverse=True)

def mark_notification_as_read(notification_id: int) -> Optional[NotificationSchema]:
    """Mark a specific notification as read."""
    notifications = load_notifications()
    for notif in notifications:
        if notif.id == notification_id:
            notif.is_read = True
            save_notifications(notifications)
            return notif
    return None
