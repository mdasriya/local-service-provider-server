from app.modules.availability.model import Availability

from app.modules.providers.model import Provider


# ======================================
# CREATE AVAILABILITY
# ======================================

def create_availability_service(
    availability_data,
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

    availability = Availability(

        provider_id=provider.id,

        day=availability_data.day,

        start_time=availability_data.start_time,

        end_time=availability_data.end_time
    )

    db.add(availability)

    db.commit()

    db.refresh(availability)

    return {
        "success": True,
        "message": "Availability created successfully",
        "data": availability
    }


# ======================================
# GET MY AVAILABILITY
# ======================================

def get_my_availability_service(
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

    availability = db.query(Availability).filter(
        Availability.provider_id == provider.id
    ).all()

    return {
        "success": True,
        "message": "Availability fetched successfully",
        "data": availability
    }


# ======================================
# GET PROVIDER AVAILABILITY
# ======================================

def get_provider_availability_service(
    provider_id,
    db
):

    availability = db.query(Availability).filter(
        Availability.provider_id == provider_id
    ).all()

    return {
        "success": True,
        "message": "Provider availability fetched successfully",
        "data": availability
    }


# ======================================
# DELETE AVAILABILITY
# ======================================

def delete_availability_service(
    availability_id,
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

    availability = db.query(Availability).filter(
        Availability.id == availability_id,
        Availability.provider_id == provider.id
    ).first()

    if not availability:

        return {
            "success": False,
            "message": "Availability slot not found"
        }

    db.delete(availability)

    db.commit()

    return {
        "success": True,
        "message": "Availability deleted successfully"
    }