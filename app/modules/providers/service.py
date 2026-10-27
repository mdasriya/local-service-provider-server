from sqlalchemy import or_, cast, String

from app.modules.bookings.model import Booking
from app.modules.providers.model import Provider
from app.modules.reviews.model import Review
from app.modules.services.model import Service
from app.modules.users.model import User



# ======================================
# CREATE PROVIDER SERVICE
# ======================================

def create_provider_service(
    provider_data,
    current_user,
    db
):

    return create_provider_for_user_service(provider_data, current_user.id, db)


def create_provider_for_user_service(provider_data, user_id, db):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"success": False, "message": "User not found"}

    existing_provider = db.query(Provider).filter(
        Provider.user_id == user_id
    ).first()

    if existing_provider:

        return {
            "success": False,
            "message": "Provider profile already exists"
        }

    # ======================================
    # CREATE PROVIDER
    # ======================================

    new_provider = Provider(

        user_id=user_id,

        bio=provider_data.bio,

        experience=provider_data.experience,

        service_area=provider_data.service_area,

        hourly_rate=provider_data.hourly_rate,
        government_id=provider_data.government_id,
        image=provider_data.image,
        provider_type=provider_data.provider_type,
        category=provider_data.category,
        city=provider_data.city,
        locality=provider_data.locality,
        service_radius=provider_data.service_radius
    )

    db.add(new_provider)

    # ======================================
    # UPDATE USER ROLE
    # ======================================

    user.role = "provider"
    if provider_data.full_name:
        user.full_name = provider_data.full_name
    if provider_data.phone:
        user.phone = provider_data.phone

    db.commit()

    db.refresh(new_provider)

    return {
        "success": True,
        "message": "Provider profile created successfully",
        "data": {
            "provider_id": new_provider.id,
            "user_id": new_provider.user_id,
            "experience": new_provider.experience,
            "service_area": new_provider.service_area,
            "category": new_provider.category,
            "provider_type": new_provider.provider_type
        }
    }


def update_provider_service(provider_id, provider_data, db):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return {"success": False, "message": "Provider not found"}

    user = db.query(User).filter(User.id == provider.user_id).first()
    if not user:
        return {"success": False, "message": "Provider user not found"}

    for field in ("bio", "experience", "service_area", "hourly_rate", "government_id", "image"):
        value = getattr(provider_data, field)
        if value is not None:
            setattr(provider, field, value)

    for field in ("full_name", "phone", "is_active"):
        value = getattr(provider_data, field)
        if value is not None:
            setattr(user, field, value)

    if provider_data.verification_status is not None:
        provider.verification_status = provider_data.verification_status.lower()

    db.commit()
    db.refresh(provider)

    return {
        "success": True,
        "message": "Provider updated successfully",
        "data": {"provider_id": provider.id, "user_id": provider.user_id}
    }

# ======================================
# GET TOP PROVIDERS
# ======================================

def get_top_providers_service(db):

    providers = db.query(Provider).order_by(
        Provider.average_rating.desc()
    ).all()

    return {
        "success": True,
        "data": providers
    }


def get_providers_service(db, page=1, limit=8, search=None, verification_status=None, status=None):
    query = db.query(Provider, User).join(User, Provider.user_id == User.id)

    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.filter(or_(
            User.full_name.ilike(search_term),
            User.email.ilike(search_term),
            User.phone.ilike(search_term),
            cast(Provider.id, String).ilike(search_term),
        ))

    if verification_status and verification_status.lower() != "all":
        query = query.filter(Provider.verification_status.ilike(verification_status))

    if status and status.lower() != "all":
        if status.lower() == "active":
            query = query.filter(User.is_active.is_(True))
        elif status.lower() in {"inactive", "suspended"}:
            query = query.filter(User.is_active.is_(False))

    total = query.count()
    provider_rows = query.order_by(Provider.created_at.desc(), Provider.id.desc()).offset((page - 1) * limit).limit(limit).all()

    providers_data = []
    for provider, user in provider_rows:
        services = db.query(Service).filter(Service.provider_id == provider.id).order_by(Service.created_at.asc()).all()
        bookings_count = db.query(Booking).filter(Booking.provider_id == provider.id).count()
        reviews_count = db.query(Review).filter(Review.provider_id == provider.id).count()
        verification = (provider.verification_status or "pending").lower()

        providers_data.append({
            "id": provider.id,
            "user_id": user.id,
            "name": user.full_name or user.email,
            "email": user.email,
            "phone": user.phone or "-",
            "primary_service": services[0].title if services else "-",
            "services": [service.title for service in services],
            "services_count": len(services),
            "city": provider.service_area or "-",
            "experience": provider.experience or 0,
            "bio": provider.bio or "",
            "hourly_rate": float(provider.hourly_rate or 0),
            "government_id": provider.government_id or "",
            "is_active": bool(user.is_active),
            "rating": float(provider.average_rating or 0),
            "reviews_count": reviews_count,
            "bookings_count": bookings_count,
            "verification_status": verification,
            "status": "active" if user.is_active else "suspended",
            "image": provider.image,
            "joined_date": provider.created_at,
        })

    all_providers = db.query(Provider, User).join(User, Provider.user_id == User.id)
    return {
        "success": True,
        "data": providers_data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        },
        "stats": {
            "total": all_providers.count(),
            "pending": all_providers.filter(Provider.verification_status.ilike("pending")).count(),
            "active": all_providers.filter(User.is_active.is_(True)).count(),
            "suspended": all_providers.filter(User.is_active.is_(False)).count(),
        },
    }

