from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import require_customer

from app.modules.favorites.schema import (
    FavoriteCreateSchema
)

from app.modules.favorites.controller import (
    add_favorite_controller,
    get_my_favorites_controller,
    remove_favorite_controller
)


router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)


# ======================================
# ADD FAVORITE
# ======================================

@router.post("/")
def add_favorite(

    favorite: FavoriteCreateSchema,

    current_user = Depends(require_customer),

    db: Session = Depends(get_db)
):

    return add_favorite_controller(
        favorite,
        current_user,
        db
    )


# ======================================
# GET MY FAVORITES
# ======================================

@router.get("/")
def get_my_favorites(

    current_user = Depends(require_customer),

    db: Session = Depends(get_db)
):

    return get_my_favorites_controller(
        current_user,
        db
    )


# ======================================
# REMOVE FAVORITE
# ======================================

@router.delete("/{service_id}")
def remove_favorite(

    service_id: int,

    current_user = Depends(require_customer),

    db: Session = Depends(get_db)
):

    return remove_favorite_controller(
        service_id,
        current_user,
        db
    )