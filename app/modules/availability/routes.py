from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import require_provider

from app.modules.availability.schema import (
    AvailabilityCreateSchema
)

from app.modules.availability.controller import (

    create_availability_controller,

    get_my_availability_controller,

    get_provider_availability_controller,

    delete_availability_controller
)


router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)


# ======================================
# CREATE AVAILABILITY
# ======================================

@router.post("/create")
def create_availability(

    availability: AvailabilityCreateSchema,

    current_user = Depends(require_provider),

    db: Session = Depends(get_db)
):

    return create_availability_controller(
        availability,
        current_user,
        db
    )


# ======================================
# GET MY AVAILABILITY
# ======================================

@router.get("/my-slots")
def get_my_availability(

    current_user = Depends(require_provider),

    db: Session = Depends(get_db)
):

    return get_my_availability_controller(
        current_user,
        db
    )


# ======================================
# GET PROVIDER AVAILABILITY
# ======================================

@router.get("/provider/{provider_id}")
def get_provider_availability(

    provider_id: int,

    db: Session = Depends(get_db)
):

    return get_provider_availability_controller(
        provider_id,
        db
    )


# ======================================
# DELETE AVAILABILITY
# ======================================

@router.delete("/{availability_id}")
def delete_availability(

    availability_id: int,

    current_user = Depends(require_provider),

    db: Session = Depends(get_db)
):

    return delete_availability_controller(
        availability_id,
        current_user,
        db
    )