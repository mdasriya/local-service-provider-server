from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.tokens.schema import RefreshTokenSchema

from app.modules.tokens.controller import (
    refresh_access_token_controller,
    logout_controller
)


router = APIRouter(
    prefix="/tokens",
    tags=["Tokens"]
)


# ======================================
# REFRESH ACCESS TOKEN
# ======================================

@router.post("/refresh")
def refresh_access_token(

    refresh_token: RefreshTokenSchema,

    db: Session = Depends(get_db)
):

    return refresh_access_token_controller(
        refresh_token,
        db
    )


# ======================================
# LOGOUT
# ======================================

@router.post("/logout")
def logout(

    refresh_token: RefreshTokenSchema,

    db: Session = Depends(get_db)
):

    return logout_controller(
        refresh_token,
        db
    )