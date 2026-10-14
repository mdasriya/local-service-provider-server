from app.modules.auth.service import (
    register_service
,  login_service
)
from app.modules.auth.service import (
    provider_dashboard_service
)


# ======================================
# REGISTER CONTROLLER
# ======================================

def register_controller(user_data, db):

    result = register_service(
        user_data,
        db
    )

    return result

# ======================================
# LOGIN CONTROLLER
# ======================================

def login_controller(login_data, db):

    result = login_service(
        login_data,
        db
    )

    return result


# ======================================
# CURRENT USER CONTROLLER
# ======================================

def current_user_controller(current_user):

    return {
        "success": True,
        "message": "Current user fetched successfully",
        "data": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "phone": current_user.phone,
            "role": current_user.role
        }
    }




# ======================================
# PROVIDER DASHBOARD
# ======================================

def provider_dashboard_controller(
    current_user,
    db
):

    return provider_dashboard_service(
        current_user,
        db
    )