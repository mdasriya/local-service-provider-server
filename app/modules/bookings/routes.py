from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import (
    get_current_user,
    require_provider,
    require_admin
)

from app.modules.bookings.schema import (
    BookingCreateSchema
)

from app.modules.bookings.controller import (
    create_booking_controller,
    get_my_bookings_controller,
    get_provider_bookings_controller,
    update_booking_status_controller
    , get_admin_bookings_controller
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("/admin")
def get_admin_bookings(page: int = 1, limit: int = 8, search: str | None = None, status: str | None = None, service_id: str | None = None, date_from: str | None = None, date_to: str | None = None, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return get_admin_bookings_controller(db, page, limit, search, status, service_id, date_from, date_to)


# ======================================
# CREATE BOOKING
# ======================================

@router.post("/")
def create_booking(

    booking: BookingCreateSchema,

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)
):

    return create_booking_controller(
        booking,
        current_user,
        db
    )


# ======================================
# GET MY BOOKINGS
# ======================================

@router.get("/my")
def get_my_bookings(

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)
):

    return get_my_bookings_controller(
        current_user,
        db
    )

# ======================================
# GET PROVIDER BOOKINGS
# ======================================

@router.get("/provider")
def get_provider_bookings(

    db: Session = Depends(get_db),

    current_user = Depends(require_provider)
):

    return get_provider_bookings_controller(
        current_user,
        db
    )


# ======================================
# UPDATE BOOKING STATUS
# ======================================

@router.put("/{booking_id}/status")
def update_booking_status(

    booking_id: int,

    status: str,

    db: Session = Depends(get_db),

    current_user = Depends(require_provider)
):

    return update_booking_status_controller(
        booking_id,
        status,
        current_user,
        db
    )