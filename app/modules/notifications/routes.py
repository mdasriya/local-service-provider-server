from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import get_current_user

from app.modules.notifications.controller import (
    get_my_notifications_controller,
    mark_notification_read_controller
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# ======================================
# GET MY NOTIFICATIONS
# ======================================

@router.get("/")
def get_my_notifications(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_my_notifications_controller(
        current_user,
        db
    )


# ======================================
# MARK NOTIFICATION AS READ
# ======================================

@router.put("/read/{notification_id}")
def mark_notification_read(
    notification_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return mark_notification_read_controller(
        notification_id,
        current_user,
        db
    )