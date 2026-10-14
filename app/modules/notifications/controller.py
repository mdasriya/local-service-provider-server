from app.modules.notifications.service import (
    get_my_notifications_service,
    mark_notification_read_service
)


# ======================================
# GET MY NOTIFICATIONS CONTROLLER
# ======================================

def get_my_notifications_controller(
    current_user,
    db
):

    return get_my_notifications_service(
        current_user,
        db
    )


# ======================================
# MARK NOTIFICATION READ CONTROLLER
# ======================================

def mark_notification_read_controller(
    notification_id,
    current_user,
    db
):

    return mark_notification_read_service(
        notification_id,
        current_user,
        db
    )