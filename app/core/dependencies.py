from ipaddress import ip_address
from os import getenv

from fastapi import Depends, HTTPException
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.security import verify_access_token

from app.modules.users.model import User


security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def _get_user_from_credentials(
    credentials: HTTPAuthorizationCredentials,
    db: Session
):
    payload = verify_access_token(credentials.credentials)

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
# GET CURRENT USER
# ======================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return _get_user_from_credentials(credentials, db)

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


def require_admin_or_local_development(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
    db: Session = Depends(get_db)
):
    client = request.client
    if getenv("APP_ENV", "").lower() == "development" and client is not None:
        try:
            if ip_address(client.host).is_loopback:
                return None
        except ValueError:
            pass

    if credentials is None:
        raise HTTPException(
            status_code=403,
            detail="Not authenticated"
        )

    current_user = _get_user_from_credentials(credentials, db)

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