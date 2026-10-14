from datetime import datetime, timedelta, timezone

from uuid import uuid4
import random

from app.modules.users.model import User

from app.core.security import hash_password


# ======================================
# FORGOT PASSWORD SERVICE
# ======================================

def forgot_password_service(forgot_data, db):

    user = db.query(User).filter(
        User.email == forgot_data.email
    ).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    otp = str(random.randint(100000, 999999))

    user.reset_otp = otp
    user.reset_otp_expiry = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=10)

    db.commit()

    return {
        "success": True,
        "message": "OTP generated successfully",
        "otp": otp
    }


def reset_password_service(reset_data, db):

    user = db.query(User).filter(
        User.email == reset_data.email
    ).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    if user.reset_otp != reset_data.otp:
        return {
            "success": False,
            "message": "Invalid OTP"
        }

    if user.reset_otp_expiry < datetime.now(timezone.utc).replace(tzinfo=None):
        return {
            "success": False,
            "message": "OTP expired"
        }

    user.password = hash_password(reset_data.new_password)
    user.reset_otp = None
    user.reset_otp_expiry = None

    db.commit()

    return {
        "success": True,
        "message": "Password reset successfully"
    }