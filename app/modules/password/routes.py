from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.password.schema import (
    ForgotPasswordSchema,
    ResetPasswordSchema
)

from app.modules.password.controller import (
    forgot_password_controller,
    reset_password_controller
)


router = APIRouter(
    prefix="/password",
    tags=["Password"]
)


# ======================================
# FORGOT PASSWORD
# ======================================

@router.post("/forgot")
def forgot_password(
    forgot_data: ForgotPasswordSchema,
    db: Session = Depends(get_db)
):

    return forgot_password_controller(
        forgot_data,
        db
    )


# ======================================
# RESET PASSWORD
# ======================================

@router.post("/reset")
def reset_password(
    reset_data: ResetPasswordSchema,
    db: Session = Depends(get_db)
):

    return reset_password_controller(
        reset_data,
        db
    )