from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import (
    require_provider,
    get_current_user,
    require_admin
)

from app.modules.services.schema import (
    ServiceCreateSchema,
    AdminServiceCreateSchema
)

from app.modules.services.controller import (
    create_service_controller,
    create_admin_service_controller,
    get_services_controller,
    search_services_controller
)

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


# ======================================
# CREATE SERVICE
# ======================================

@router.post("/admin")
def create_admin_service(
    service: AdminServiceCreateSchema,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return create_admin_service_controller(service, db)

@router.post("/")
def create_service(

    service: ServiceCreateSchema,

    db: Session = Depends(get_db),

    current_user = Depends(require_provider)
):

    return create_service_controller(
        service,
        current_user,
        db
    )


# ======================================
# GET ALL SERVICES
# ======================================

@router.get("/")
def get_services(
    page: int = Query(1, ge=1),
    limit: int = Query(8, ge=1, le=100),
    search: str | None = Query(None),
    category_id: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db)
):

    return get_services_controller(db, page, limit, search, category_id, status)


# ======================================
# SEARCH SERVICES
# ======================================

@router.get("/search")
def search_services(

    keyword: str = None,

    category_id: int = None,

    min_price: float = None,

    max_price: float = None,

    sort_by: str = None,

    page: int = 1,

    limit: int = 10,

    db: Session = Depends(get_db)
):

    return search_services_controller(
        db,
        keyword,
        category_id,
        min_price,
        max_price,
        sort_by,
        page,
        limit
    )