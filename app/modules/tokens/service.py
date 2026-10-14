from datetime import datetime, timezone

from app.modules.tokens.model import RefreshToken
from app.modules.users.model import User

from app.core.security import (
    verify_refresh_token,
    create_access_token
)


# ======================================
# REFRESH ACCESS TOKEN SERVICE
# ======================================

def refresh_access_token_service(
    refresh_token_data,
    db
):

    token = refresh_token_data.refresh_token

    payload = verify_refresh_token(token)

    if not payload:

        return {
            "success": False,
            "message": "Invalid or expired refresh token"
        }

    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.is_revoked == False
    ).first()

    if not stored_token:

        return {
            "success": False,
            "message": "Refresh token revoked or not found"
        }

    if stored_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):

        return {
            "success": False,
            "message": "Refresh token expired"
        }

    user = db.query(User).filter(
        User.id == payload.get("user_id")
    ).first()

    if not user:

        return {
            "success": False,
            "message": "User not found"
        }

    new_access_token = create_access_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    })

    return {
        "success": True,
        "message": "Access token refreshed successfully",
        "data": {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    }


# ======================================
# LOGOUT SERVICE
# ======================================

def logout_service(
    refresh_token_data,
    db
):

    token = refresh_token_data.refresh_token

    stored_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not stored_token:

        return {
            "success": False,
            "message": "Refresh token not found"
        }

    stored_token.is_revoked = True

    db.commit()

    return {
        "success": True,
        "message": "Logged out successfully"
    }