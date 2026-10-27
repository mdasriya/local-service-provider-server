from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import (get_current_user,require_admin,require_provider,require_customer)

from app.database.session import get_db
from app.modules.users.model import User

from app.modules.auth.schema import (
    RegisterSchema,
    LoginSchema,
)

from app.modules.auth.controller import (
    register_controller
, login_controller,
 current_user_controller, 
provider_dashboard_controller
)
from app.modules.auth.service import register_admin_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ======================================
# REGISTER API
# ======================================

@router.post("/register")
def register(user: RegisterSchema,db: Session = Depends(get_db)):
    return register_controller(
        user,
        db
    )


@router.post("/register-admin")
def register_admin(user: RegisterSchema, db: Session = Depends(get_db)):
    result = register_admin_service(user, db)
    if result.get("success") is False:
        raise HTTPException(status_code=409, detail=result["message"])
    return result


# ======================================
# LOGIN API
# ======================================

@router.post("/login")
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):

    return login_controller(
        user,
        db
    )


# ======================================
# CURRENT USER API
# ======================================

@router.get("/me")
def get_me(
    current_user = Depends(get_current_user)
):

    return current_user_controller(
        current_user
    )





# ======================================
# PROVIDER ONLY API
# ======================================


# ======================================
# PROVIDER DASHBOARD
# ======================================

@router.get("/provider-dashboard")
def provider_dashboard(

    current_user = Depends(require_provider),

    db: Session = Depends(get_db)
):

    return provider_dashboard_controller(
        current_user,
        db
    )


# ======================================
# CUSTOMER ONLY API
# ======================================

@router.get("/customer-dashboard")
def customer_dashboard(
    current_user = Depends(require_customer)
):

    return {
        "success": True,
        "message": "Welcome Customer",
        "user": current_user.full_name
    }


# ======================================
# TEMP MAKE ADMIN
# ======================================

@router.put("/make-admin/{user_id}", dependencies=[Depends(require_admin)])
def make_admin(

    user_id: int,

    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "success": False,
            "message": "User not found"
        }

    user.role = "admin"

    db.commit()

    return {
        "success": True,
        "message": "User is now admin"
    }
