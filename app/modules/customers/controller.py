from sqlalchemy.orm import Session

from app.modules.customers.service import (
    get_customer_dashboard_service
)


# ======================================
# CUSTOMER DASHBOARD CONTROLLER
# ======================================

def get_customer_dashboard_controller(

    current_user,

    db: Session
):

    return get_customer_dashboard_service(
        current_user,
        db
    )