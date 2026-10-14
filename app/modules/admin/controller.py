from sqlalchemy.orm import Session
from app.modules.admin.service import get_dashboard_service


# ======================================
# DASHBOARD CONTROLLER
# ======================================

def get_dashboard_controller(db: Session, range_days=7):

    return get_dashboard_service(db, range_days)