from app.modules.bookings.service import (
    create_booking_service,
    get_my_bookings_service,
    update_booking_status_service,
    get_provider_bookings_service,
    get_admin_bookings_service
)


# ======================================
# CREATE BOOKING CONTROLLER
# ======================================

def create_booking_controller(

    booking_data,

    current_user,

    db
):

    return create_booking_service(
        booking_data,
        current_user,
        db
    )


# ======================================
# GET MY BOOKINGS
# ======================================

def get_my_bookings_controller(

    current_user,

    db
):

    return get_my_bookings_service(
        current_user,
        db
    )


# ======================================
# GET PROVIDER BOOKINGS
# ======================================

def get_provider_bookings_controller(

    current_user,

    db
):

    return get_provider_bookings_service(
        current_user,
        db
    )


# ======================================
# UPDATE BOOKING STATUS
# ======================================

def update_booking_status_controller(

    booking_id,

    status,

    current_user,

    db
):

    return update_booking_status_service(
        booking_id,
        status,
        current_user,
        db
    )


def get_admin_bookings_controller(db, page=1, limit=8, search=None, status=None, service_id=None, date_from=None, date_to=None):
    return get_admin_bookings_service(db, page, limit, search, status, service_id, date_from, date_to)