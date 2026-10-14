from app.modules.services.model import Service
from app.modules.providers.model import Provider
from app.modules.bookings.model import Booking
from app.modules.users.model import User
from sqlalchemy import or_, cast, String
from datetime import datetime

from app.modules.availability.model import Availability
from app.modules.notifications.service import create_notification_service



# ======================================
# CREATE BOOKING
# ======================================

def create_booking_service(

    booking_data,

    current_user,

    db
):

    # ======================================
    # FIND SERVICE
    # ======================================

    service = db.query(Service).filter(
        Service.id == booking_data.service_id
    ).first()

    if not service:

        return {
            "success": False,
            "message": "Service not found"
        }

    # ======================================
    # GET BOOKING DAY
    # ======================================

    booking_day = booking_data.booking_date.strftime("%A")

    # ======================================
    # CHECK PROVIDER AVAILABILITY
    # ======================================

    availability = db.query(Availability).filter(

        Availability.provider_id == service.provider_id,

        Availability.day == booking_day,

        Availability.start_time <= booking_data.booking_time,

        Availability.end_time >= booking_data.booking_time,

        Availability.is_available == True

    ).first()

    if not availability:

        return {
            "success": False,
            "message": "Provider not available at selected time"
        }

    # ======================================
    # CHECK DOUBLE BOOKING
    # ======================================

    existing_booking = db.query(Booking).filter(

        Booking.provider_id == service.provider_id,

        Booking.booking_date == booking_data.booking_date,

        Booking.booking_time == booking_data.booking_time,

        Booking.status.in_(["pending", "accepted"])

    ).first()

    if existing_booking:

        return {
            "success": False,
            "message": "This slot is already booked"
        }

    # ======================================
    # CREATE BOOKING
    # ======================================

    new_booking = Booking(

        customer_id=current_user.id,

        provider_id=service.provider_id,

        service_id=service.id,

        booking_date=booking_data.booking_date,

        booking_time=booking_data.booking_time,

        address=booking_data.address,

        total_price=service.price,

        status="pending"
    )

    db.add(new_booking)

    db.commit()

    db.refresh(new_booking)

    provider = db.query(Provider).filter(
    Provider.id == service.provider_id
    ).first()

    if provider:

     create_notification_service(
        user_id=provider.user_id,
        title="New Booking Received",
        message="You have received a new booking request.",
        db=db
     )

    return {
        "success": True,
        "message": "Booking created successfully",
        "data": {

            "booking_id": new_booking.id,

            "service_id": service.id,

            "provider_id": service.provider_id,

            "booking_date": new_booking.booking_date,

            "booking_time": new_booking.booking_time,

            "status": new_booking.status
        }
    }


# ======================================
# GET MY BOOKINGS
# ======================================

def get_my_bookings_service(

    current_user,

    db
):

    bookings = db.query(Booking).filter(
        Booking.customer_id == current_user.id
    ).all()

    return {
        "success": True,
        "data": bookings
    }

# ======================================
# GET PROVIDER BOOKINGS
# ======================================

def get_provider_bookings_service(

    current_user,

    db
):

    # FIND PROVIDER PROFILE

    provider = db.query(Provider).filter(
        Provider.user_id == current_user.id
    ).first()

    if not provider:

        return {
            "success": False,
            "message": "Provider profile not found"
        }

    # GET BOOKINGS

    bookings = db.query(Booking).filter(
        Booking.provider_id == provider.id
    ).all()

    return {
        "success": True,
        "data": bookings
    }


# ======================================
# UPDATE BOOKING STATUS
# ======================================

def update_booking_status_service(

    booking_id,

    status,

    current_user,

    db
):

    # FIND PROVIDER

    provider = db.query(Provider).filter(
        Provider.user_id == current_user.id
    ).first()

    if not provider:

        return {
            "success": False,
            "message": "Provider profile not found"
        }

    # FIND BOOKING

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        return {
            "success": False,
            "message": "Booking not found"
        }

    # OWNERSHIP VALIDATION

    if booking.provider_id != provider.id:

        return {
            "success": False,
            "message": "Unauthorized booking access"
        }

    # VALID STATUSES

    valid_statuses = [
        "accepted",
        "rejected",
        "completed"
    ]

    if status not in valid_statuses:

        return {
            "success": False,
            "message": "Invalid booking status"
        }

    # UPDATE STATUS

    booking.status = status

    db.commit()

    db.refresh(booking)

    return {
        "success": True,
        "message": f"Booking {status} successfully",
        "data": {
            "booking_id": booking.id,
            "status": booking.status
        }
    }

# ======================================
# UPDATE BOOKING STATUS
# ======================================

def update_booking_status_service(

    booking_id,

    status,

    current_user,

    db
):

    # FIND PROVIDER

    provider = db.query(Provider).filter(
        Provider.user_id == current_user.id
    ).first()

    if not provider:

        return {
            "success": False,
            "message": "Provider profile not found"
        }

    # FIND BOOKING

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        return {
            "success": False,
            "message": "Booking not found"
        }

    # OWNERSHIP VALIDATION

    if booking.provider_id != provider.id:

        return {
            "success": False,
            "message": "Unauthorized booking access"
        }

    # VALID STATUSES

    valid_statuses = [
        "accepted",
        "rejected",
        "completed"
    ]

    if status not in valid_statuses:

        return {
            "success": False,
            "message": "Invalid booking status"
        }

    # UPDATE STATUS

    booking.status = status

    db.commit()

    db.refresh(booking)

    return {
        "success": True,
        "message": f"Booking {status} successfully",
        "data": {
            "booking_id": booking.id,
            "status": booking.status
        }
    }


def get_admin_bookings_service(db, page=1, limit=8, search=None, status=None, service_id=None, date_from=None, date_to=None):
    query = db.query(Booking, User, Provider, Service).join(User, Booking.customer_id == User.id).join(Provider, Booking.provider_id == Provider.id).join(Service, Booking.service_id == Service.id)

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(or_(cast(Booking.id, String).ilike(term), User.full_name.ilike(term), User.email.ilike(term), Service.title.ilike(term)))
    if status and status.lower() != "all":
        query = query.filter(Booking.status.ilike(status))
    if service_id and service_id != "all":
        query = query.filter(Booking.service_id == int(service_id))
    if date_from:
        query = query.filter(Booking.booking_date >= date_from)
    if date_to:
        query = query.filter(Booking.booking_date <= date_to)

    total = query.count()
    rows = query.order_by(Booking.booking_date.desc(), Booking.booking_time.desc(), Booking.id.desc()).offset((page - 1) * limit).limit(limit).all()
    data = []
    for booking, customer, provider, service in rows:
        provider_user = db.query(User).filter(User.id == provider.user_id).first()
        data.append({
            "id": booking.id,
            "booking_id": f"BK-{booking.id:04d}",
            "customer_name": customer.full_name or customer.email,
            "customer_email": customer.email,
            "provider_name": provider_user.full_name if provider_user else "-",
            "service_name": service.title,
            "price": float(booking.total_price or 0),
            "status": booking.status,
            "booking_date": booking.booking_date,
            "booking_time": booking.booking_time,
            "updated_at": booking.created_at,
        })
    return {"success": True, "data": data, "pagination": {"page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit}}