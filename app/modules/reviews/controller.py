from app.modules.reviews.service import (
    create_review_service,
    get_provider_reviews_service
)


# ======================================
# CREATE REVIEW
# ======================================

def create_review_controller(

    review_data,

    current_user,

    db
):

    return create_review_service(
        review_data,
        current_user,
        db
    )


# ======================================
# GET PROVIDER REVIEWS
# ======================================

def get_provider_reviews_controller(

    provider_id,

    db
):

    return get_provider_reviews_service(
        provider_id,
        db
    )