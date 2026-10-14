from app.modules.users.model import User
from app.modules.tokens.model import RefreshToken
from datetime import datetime, timedelta

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from sqlalchemy import func

from app.modules.providers.model import Provider
from app.modules.services.model import Service
from app.modules.bookings.model import Booking
from app.modules.reviews.model import Review


# ======================================
# REGISTER SERVICE
# ======================================

def register_service(user_data, db):

    # ======================================
    # CHECK EMAIL
    # ======================================

    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_email:

        return {
            "success": False,
            "message": "Email already exists"
        }

    # ======================================
    # HASH PASSWORD
    # ======================================

    hashed_password = hash_password(
        user_data.password
    )

    # ======================================
    # CREATE USER
    # ======================================

    new_user = User(
        email=user_data.email,
        password=hashed_password,
        role=user_data.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "success": True,
        "message": "User registered successfully",
        "data": {
            "id": new_user.id,
            "email": new_user.email,
            "role": new_user.role
        }
    }


# ======================================
# LOGIN SERVICE
# ======================================


# ======================================
# LOGIN SERVICE
# ======================================

def login_service(login_data, db):

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:

        return {
            "success": False,
            "message": "Invalid email or password"
        }

    is_password_correct = verify_password(
        login_data.password,
        user.password
    )

    if not is_password_correct:

        return {
            "success": False,
            "message": "Invalid email or password"
        }

    # ======================================
    # CREATE ACCESS TOKEN
    # ======================================

    access_token = create_access_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    })

    # ======================================
    # CREATE REFRESH TOKEN
    # ======================================

    refresh_token = create_refresh_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    })

    # ======================================
    # SAVE REFRESH TOKEN IN DB
    # ======================================

    refresh_token_record = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    db.add(refresh_token_record)

    db.commit()

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": getattr(user, "full_name", None),
                "email": user.email,
                "role": user.role
            }
        }
    }


# ======================================
# PROVIDER DASHBOARD SERVICE
# ======================================

def provider_dashboard_service(
    current_user,
    db
):

    provider = db.query(Provider).filter(
        Provider.user_id == current_user.id
    ).first()

    if not provider:

        return {
            "success": False,
            "message": "Provider profile not found"
        }

    total_services = db.query(Service).filter(
        Service.provider_id == provider.id
    ).count()

    total_bookings = db.query(Booking).filter(
        Booking.provider_id == provider.id
    ).count()

    completed_bookings = db.query(Booking).filter(
        Booking.provider_id == provider.id,
        Booking.status == "completed"
    ).count()

    pending_bookings = db.query(Booking).filter(
        Booking.provider_id == provider.id,
        Booking.status == "pending"
    ).count()

    total_reviews = db.query(Review).filter(
        Review.provider_id == provider.id
    ).count()

    average_rating = db.query(
        func.avg(Review.rating)
    ).filter(
        Review.provider_id == provider.id
    ).scalar()

    return {
        "success": True,
        "message": "Provider dashboard fetched successfully",

        "provider": {
            "provider_id": provider.id,
            "full_name": getattr(current_user, "full_name", None),
            "email": current_user.email,
            "phone": getattr(current_user, "phone", None),
            "bio": provider.bio,
            "experience": provider.experience,
            "service_area": provider.service_area,
            "hourly_rate": provider.hourly_rate,
            "verification_status": provider.verification_status
        },

        "statistics": {
            "total_services": total_services,
            "total_bookings": total_bookings,
            "completed_bookings": completed_bookings,
            "pending_bookings": pending_bookings,
            "total_reviews": total_reviews,
            "average_rating": round(average_rating, 1) if average_rating else 0
        }
    }