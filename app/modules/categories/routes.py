from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.categories.schema import (
    CategoryCreateSchema,
    CategoryUpdateSchema
)

from app.modules.categories.controller import (
    create_category_controller,
    get_categories_controller,
    update_category_controller,
    delete_category_controller
)

from app.core.dependencies import (
    require_admin
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# ======================================
# CREATE CATEGORY
# ADMIN ONLY
# ======================================

@router.post("/")
def create_category(
    category: CategoryCreateSchema,

    db: Session = Depends(get_db),

    current_user = Depends(require_admin)
):

    return create_category_controller(
        category,
        db
    )


# ======================================
# GET ALL CATEGORIES
# ======================================

@router.get("/")
def get_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(8, ge=1, le=100),
    search: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db)
):

    return get_categories_controller(db, page, limit, search, status)


@router.put("/{category_id}")
def update_category(
    category_id: int,
    category: CategoryUpdateSchema,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return update_category_controller(category_id, category, db)


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return delete_category_controller(category_id, db)