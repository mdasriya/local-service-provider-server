from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import (
    get_current_user
)

from app.modules.reviews.schema import (
    ReviewCreateSchema
)

from app.modules.reviews.controller import (
    create_review_controller,
    get_provider_reviews_controller
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


# ======================================
# CREATE REVIEW
# ======================================

@router.post("/")
def create_review(

    review: ReviewCreateSchema,

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)
):

    return create_review_controller(
        review,
        current_user,
        db
    )


# ======================================
# GET PROVIDER REVIEWS
# ======================================

@router.get("/provider/{provider_id}")
def get_provider_reviews(

    provider_id: int,

    db: Session = Depends(get_db)
):

    return get_provider_reviews_controller(
        provider_id,
        db
    )