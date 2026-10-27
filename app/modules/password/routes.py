from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.email import EmailConfigurationError, EmailDeliveryError
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
    try:
        return forgot_password_controller(forgot_data, db)
    except EmailConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except EmailDeliveryError as error:
        raise HTTPException(
            status_code=503,
            detail="Could not deliver the password reset email. Please try again later.",
        ) from error


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