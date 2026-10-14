from app.modules.favorites.model import Favorite
from app.modules.services.model import Service


# ======================================
# ADD FAVORITE SERVICE
# ======================================

def add_favorite_service(

    favorite_data,

    current_user,

    db
):

    # CHECK SERVICE

    service = db.query(Service).filter(
        Service.id == favorite_data.service_id
    ).first()

    if not service:

        return {
            "success": False,
            "message": "Service not found"
        }

    # CHECK DUPLICATE FAVORITE

    existing_favorite = db.query(Favorite).filter(
        Favorite.customer_id == current_user.id,
        Favorite.service_id == favorite_data.service_id
    ).first()

    if existing_favorite:

        return {
            "success": False,
            "message": "Service already in favorites"
        }

    # CREATE FAVORITE

    favorite = Favorite(
        customer_id=current_user.id,
        service_id=favorite_data.service_id
    )

    db.add(favorite)

    db.commit()

    db.refresh(favorite)

    return {
        "success": True,
        "message": "Service added to favorites"
    }


# ======================================
# GET MY FAVORITES
# ======================================

def get_my_favorites_service(

    current_user,

    db
):

    favorites = db.query(Favorite).filter(
        Favorite.customer_id == current_user.id
    ).all()

    return {
        "success": True,
        "data": favorites
    }


# ======================================
# REMOVE FAVORITE
# ======================================

def remove_favorite_service(

    service_id,

    current_user,

    db
):

    favorite = db.query(Favorite).filter(
        Favorite.customer_id == current_user.id,
        Favorite.service_id == service_id
    ).first()

    if not favorite:

        return {
            "success": False,
            "message": "Favorite not found"
        }

    db.delete(favorite)

    db.commit()

    return {
        "success": True,
        "message": "Favorite removed successfully"
    }