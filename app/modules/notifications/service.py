from app.modules.notifications.model import Notification


# ======================================
# CREATE NOTIFICATION SERVICE
# ======================================

def create_notification_service(
    user_id,
    title,
    message,
    db
):

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message
    )

    db.add(notification)

    db.commit()

    db.refresh(notification)

    return notification


# ======================================
# GET MY NOTIFICATIONS SERVICE
# ======================================

def get_my_notifications_service(
    current_user,
    db
):

    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return {
        "success": True,
        "message": "Notifications fetched successfully",
        "data": notifications
    }


# ======================================
# MARK NOTIFICATION AS READ SERVICE
# ======================================

def mark_notification_read_service(
    notification_id,
    current_user,
    db
):

    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:

        return {
            "success": False,
            "message": "Notification not found"
        }

    notification.is_read = True

    db.commit()

    db.refresh(notification)

    return {
        "success": True,
        "message": "Notification marked as read"
    }