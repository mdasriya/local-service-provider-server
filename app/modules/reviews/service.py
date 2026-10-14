from app.modules.bookings.model import Booking

from app.modules.reviews.model import Review
from sqlalchemy import func

from app.modules.providers.model import Provider


# ======================================
# CREATE REVIEW
# ======================================

def create_review_service(

    review_data,

    current_user,

    db
):

    # FIND BOOKING

    booking = db.query(Booking).filter(
        Booking.id == review_data.booking_id
    ).first()

    if not booking:

        return {
            "success": False,
            "message": "Booking not found"
        }

    # ONLY BOOK OWNER CAN REVIEW

    if booking.customer_id != current_user.id:

        return {
            "success": False,
            "message": "Unauthorized review access"
        }

    # ONLY COMPLETED BOOKINGS

    if booking.status != "completed":

        return {
            "success": False,
            "message": "Only completed bookings can be reviewed"
        }

    # VALIDATE RATING

    if review_data.rating < 1 or review_data.rating > 5:

        return {
            "success": False,
            "message": "Rating must be between 1 and 5"
        }

    # CHECK EXISTING REVIEW

    existing_review = db.query(Review).filter(
        Review.booking_id == booking.id
    ).first()

    if existing_review:

        return {
            "success": False,
            "message": "Review already submitted"
        }

    # CREATE REVIEW

    new_review = Review(

        booking_id=booking.id,

        customer_id=current_user.id,

        provider_id=booking.provider_id,

        service_id=booking.service_id,

        rating=review_data.rating,

        comment=review_data.comment
    )

    db.add(new_review)

    db.commit()

    db.refresh(new_review)

    # UPDATE PROVIDER RATING

    update_provider_rating(
    booking.provider_id,
    db
    )

    return {
        "success": True,
        "message": "Review submitted successfully",
        "data": {
            "review_id": new_review.id,
            "rating": new_review.rating
        }
    }


# ======================================
# GET PROVIDER REVIEWS
# ======================================

def get_provider_reviews_service(

    provider_id,

    db
):

    reviews = db.query(Review).filter(
        Review.provider_id == provider_id
    ).all()

    return {
        "success": True,
        "data": reviews
    }

# ======================================
# UPDATE PROVIDER RATINGS
# ======================================

def update_provider_rating(

    provider_id,

    db
):

    # GET AVG RATING

    average_rating = db.query(
        func.avg(Review.rating)
    ).filter(
        Review.provider_id == provider_id
    ).scalar()

    # GET TOTAL REVIEWS

    total_reviews = db.query(
        func.count(Review.id)
    ).filter(
        Review.provider_id == provider_id
    ).scalar()

    # FIND PROVIDER

    provider = db.query(Provider).filter(
        Provider.id == provider_id
    ).first()

    if provider:

        provider.average_rating = round(
            float(average_rating or 0),
            1
        )

        provider.total_reviews = total_reviews

        db.commit()