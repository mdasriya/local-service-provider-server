from app.modules.availability.service import (

    create_availability_service,

    get_my_availability_service,

    get_provider_availability_service,

    delete_availability_service
)


# ======================================
# CREATE AVAILABILITY
# ======================================

def create_availability_controller(
    availability_data,
    current_user,
    db
):

    return create_availability_service(
        availability_data,
        current_user,
        db
    )


# ======================================
# GET MY AVAILABILITY
# ======================================

def get_my_availability_controller(
    current_user,
    db
):

    return get_my_availability_service(
        current_user,
        db
    )


# ======================================
# GET PROVIDER AVAILABILITY
# ======================================

def get_provider_availability_controller(
    provider_id,
    db
):

    return get_provider_availability_service(
        provider_id,
        db
    )


# ======================================
# DELETE AVAILABILITY
# ======================================

def delete_availability_controller(
    availability_id,
    current_user,
    db
):

    return delete_availability_service(
        availability_id,
        current_user,
        db
    )