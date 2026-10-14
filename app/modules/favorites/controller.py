from app.modules.favorites.service import (
    add_favorite_service,
    get_my_favorites_service,
    remove_favorite_service
)


# ======================================
# ADD FAVORITE CONTROLLER
# ======================================

def add_favorite_controller(
    favorite_data,
    current_user,
    db
):

    return add_favorite_service(
        favorite_data,
        current_user,
        db
    )


# ======================================
# GET MY FAVORITES CONTROLLER
# ======================================

def get_my_favorites_controller(
    current_user,
    db
):

    return get_my_favorites_service(
        current_user,
        db
    )


# ======================================
# REMOVE FAVORITE CONTROLLER
# ======================================

def remove_favorite_controller(
    service_id,
    current_user,
    db
):

    return remove_favorite_service(
        service_id,
        current_user,
        db
    )