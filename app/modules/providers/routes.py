from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import (
    get_current_user,
    require_admin
)

from app.modules.providers.schema import (
    ProviderCreateSchema,
    AdminProviderCreateSchema,
    AdminProviderUpdateSchema
)

from app.modules.providers.controller import (
    create_provider_controller,
    create_admin_provider_controller,
    update_provider_controller,
    get_top_providers_controller,
    get_providers_controller
)

router = APIRouter(
    prefix="/providers",
    tags=["Providers"]
)


@router.get("/")
def get_providers(
    page: int = Query(1, ge=1),
    limit: int = Query(8, ge=1, le=100),
    search: str | None = Query(None),
    verification_status: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_providers_controller(db, page, limit, search, verification_status, status)


# ======================================
# CREATE PROVIDER PROFILE
# ======================================

@router.post("/admin")
def create_admin_provider(
    provider: AdminProviderCreateSchema,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return create_admin_provider_controller(provider, db)

@router.post("/")
def create_provider(
    provider: ProviderCreateSchema,

    db: Session = Depends(get_db),

    current_user = Depends(get_current_user)
):

    return create_provider_controller(
        provider,
        current_user,
        db
    )


@router.put("/{provider_id}")
def update_provider(
    provider_id: int,
    provider: AdminProviderUpdateSchema,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    return update_provider_controller(provider_id, provider, db)

# ======================================
# TOP PROVIDERS
# ======================================

@router.get("/top")
def get_top_providers(

    db: Session = Depends(get_db)
):

    return get_top_providers_controller(db)
