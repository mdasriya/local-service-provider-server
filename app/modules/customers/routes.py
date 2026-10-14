from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import (
    require_customer
)

from app.modules.customers.controller import (
    get_customer_dashboard_controller
)

router = APIRouter(

    prefix="/customers",

    tags=["Customers"]
)


# ======================================
# CUSTOMER DASHBOARD
# ======================================

@router.get("/dashboard")
def get_dashboard(

    current_user = Depends(require_customer),

    db: Session = Depends(get_db)
):

    return get_customer_dashboard_controller(
        current_user,
        db
    )