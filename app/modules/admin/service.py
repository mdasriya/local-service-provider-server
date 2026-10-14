from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.users.model import User
from app.modules.providers.model import Provider
from app.modules.services.model import Service
from app.modules.bookings.model import Booking


# ======================================
# ADMIN DASHBOARD
# ======================================

def get_dashboard_service(db: Session, range_days=7):

    total_users = db.query(User).count()

    total_providers = db.query(Provider).count()

    total_services = db.query(Service).count()

    total_bookings = db.query(Booking).count()

    # ======================================
    # TOTAL REVENUE
    # ======================================

    total_revenue = db.query(func.coalesce(func.sum(Booking.total_price), 0)).filter(
        Booking.status == "completed"
    ).scalar()

    today = date.today()
    start_date = today - timedelta(days=range_days - 1)
    activity_rows = db.query(Booking.booking_date, func.count(Booking.id)).filter(
        Booking.booking_date >= start_date,
        Booking.booking_date <= today
    ).group_by(Booking.booking_date).all()
    activity_counts = {str(day): count for day, count in activity_rows}
    booking_activity = [
        {"day": (start_date + timedelta(days=offset)).isoformat(), "bookings": activity_counts.get((start_date + timedelta(days=offset)).isoformat(), 0)}
        for offset in range(range_days)
    ]

    recent_rows = db.query(Booking, User, Provider, Service).join(
        User, Booking.customer_id == User.id
    ).join(Provider, Booking.provider_id == Provider.id).join(
        Service, Booking.service_id == Service.id
    ).order_by(Booking.created_at.desc(), Booking.id.desc()).limit(8).all()
    recent_bookings = []
    for booking, customer, provider, service in recent_rows:
        provider_user = db.query(User).filter(User.id == provider.user_id).first()
        recent_bookings.append({
            "id": booking.id,
            "booking_id": f"BK-{booking.id:04d}",
            "customer_name": customer.full_name or customer.email,
            "customer_email": customer.email,
            "provider_name": provider_user.full_name if provider_user else "-",
            "service_name": service.title,
            "status": booking.status,
            "booking_date": booking.booking_date,
            "booking_time": booking.booking_time,
            "total_price": float(booking.total_price or 0),
            "created_at": booking.created_at,
        })

    approval_rows = db.query(Provider.verification_status, func.count(Provider.id)).group_by(Provider.verification_status).all()
    approval_counts = {str(status or "pending").lower(): count for status, count in approval_rows}
    provider_approval = [
        {"name": "Approved", "value": approval_counts.get("verified", 0), "color": "#10B981"},
        {"name": "Pending", "value": approval_counts.get("pending", 0), "color": "#F59E0B"},
        {"name": "Rejected", "value": approval_counts.get("rejected", 0), "color": "#EF4444"},
        {"name": "Suspended", "value": db.query(Provider).join(User, Provider.user_id == User.id).filter(User.is_active.is_(False)).count(), "color": "#CBD5E1"},
    ]

    return {
        "success": True,
        "data": {
            "total_users": total_users,
            "total_providers": total_providers,
            "total_services": total_services,
            "total_bookings": total_bookings,
            "total_revenue": float(total_revenue or 0),
            "booking_activity": booking_activity,
            "provider_approval": provider_approval,
            "recent_bookings": recent_bookings,
            "activity_total": sum(item["bookings"] for item in booking_activity),
        }
    }