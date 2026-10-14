from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.security import verify_access_token

from app.modules.users.model import User


security = HTTPBearer()


# ======================================
# GET CURRENT USER
# ======================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == payload.get("user_id")
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

# ======================================
# REQUIRE ADMIN
# ======================================

def require_admin(
    current_user = Depends(get_current_user)
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


# ======================================
# REQUIRE PROVIDER
# ======================================

def require_provider(
    current_user = Depends(get_current_user)
):

    if current_user.role != "provider":

        raise HTTPException(
            status_code=403,
            detail="Provider access required"
        )

    return current_user


# ======================================
# REQUIRE CUSTOMER
# ======================================

def require_customer(
    current_user = Depends(get_current_user)
):

    if current_user.role != "customer":

        raise HTTPException(
            status_code=403,
            detail="Customer access required"
        )

    return current_user