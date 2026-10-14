from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import require_admin

from app.modules.admin.controller import (
    get_dashboard_controller
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ======================================
# DASHBOARD API
# ======================================

@router.get("/dashboard")
def get_dashboard(

    range_days: int = Query(7, ge=7, le=30),

    current_user = Depends(require_admin),

    db: Session = Depends(get_db)
):

    return get_dashboard_controller(db, range_days)