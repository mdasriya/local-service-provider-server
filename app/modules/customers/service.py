from sqlalchemy.orm import Session

from app.modules.bookings.model import Booking


# ======================================
# CUSTOMER DASHBOARD SERVICE
# ======================================

def get_customer_dashboard_service(

    current_user,

    db: Session
):

    # ======================================
    # TOTAL BOOKINGS
    # ======================================

    total_bookings = db.query(Booking).filter(
        Booking.customer_id == current_user.id
    ).count()

    # ======================================
    # PENDING BOOKINGS
    # ======================================

    pending_bookings = db.query(Booking).filter(
        Booking.customer_id == current_user.id,
        Booking.status == "pending"
    ).count()

    # ======================================
    # COMPLETED BOOKINGS
    # ======================================

    completed_bookings = db.query(Booking).filter(
        Booking.customer_id == current_user.id,
        Booking.status == "completed"
    ).count()

    # ======================================
    # CANCELLED BOOKINGS
    # ======================================

    cancelled_bookings = db.query(Booking).filter(
        Booking.customer_id == current_user.id,
        Booking.status == "cancelled"
    ).count()

    # ======================================
    # TOTAL SPENT
    # ======================================

    completed = db.query(Booking).filter(
        Booking.customer_id == current_user.id,
        Booking.status == "completed"
    ).all()

    total_spent = 0

    for booking in completed:

        total_spent += booking.total_price

    # ======================================
    # RECENT BOOKINGS
    # ======================================

    recent_bookings = db.query(Booking).filter(
        Booking.customer_id == current_user.id
    ).order_by(
        Booking.created_at.desc()
    ).limit(5).all()

    return {
        "success": True,
        "message": "Customer dashboard fetched successfully",
        "data": {
            "customer_name": current_user.full_name,
            "total_bookings": total_bookings,
            "pending_bookings": pending_bookings,
            "completed_bookings": completed_bookings,
            "cancelled_bookings": cancelled_bookings,
            "total_spent": float(total_spent),
            "recent_bookings": recent_bookings
        }
    }