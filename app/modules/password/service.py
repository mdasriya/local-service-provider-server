import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from app.core.email import (
    EmailDeliveryError,
    get_smtp_settings,
    send_password_reset_email,
)
from app.modules.users.model import User

from app.core.security import hash_password

OTP_LIFETIME = timedelta(minutes=3)
OTP_RESEND_COOLDOWN = timedelta(minutes=1)


# ======================================
# FORGOT PASSWORD SERVICE
# ======================================

def forgot_password_service(forgot_data, db):
    smtp_settings = get_smtp_settings()
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    user = db.query(User).filter(
        User.email == forgot_data.email
    ).first()

    if not user:
        return {
            "success": True,
            "message": "If an account exists for that email, a reset code has been sent."
        }

    if (
        user.reset_otp_expiry
        and user.reset_otp_expiry > now + OTP_LIFETIME - OTP_RESEND_COOLDOWN
    ):
        return {
            "success": True,
            "message": "If an account exists for that email, a reset code has been sent."
        }

    otp = f"{secrets.randbelow(1_000_000):06}"

    user.reset_otp = hashlib.sha256(otp.encode("utf-8")).hexdigest()
    user.reset_otp_expiry = now + OTP_LIFETIME
    user.reset_otp_attempts = 0

    db.commit()

    try:
        send_password_reset_email(user.email, otp, smtp_settings)
    except EmailDeliveryError:
        user.reset_otp = None
        user.reset_otp_expiry = None
        user.reset_otp_attempts = 0
        db.commit()
        raise

    return {
        "success": True,
        "message": "If an account exists for that email, a reset code has been sent."
    }


def reset_password_service(reset_data, db):

    user = db.query(User).filter(
        User.email == reset_data.email
    ).first()

    if not user:
        return {
            "success": False,
            "message": "Invalid or expired OTP"
        }

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if (
        not user.reset_otp
        or not user.reset_otp_expiry
        or user.reset_otp_expiry < now
        or user.reset_otp_attempts >= 5
    ):
        return {
            "success": False,
            "message": "Invalid or expired OTP"
        }

    otp_hash = hashlib.sha256(reset_data.otp.encode("utf-8")).hexdigest()
    if not hmac.compare_digest(user.reset_otp, otp_hash):
        user.reset_otp_attempts += 1
        if user.reset_otp_attempts >= 5:
            user.reset_otp = None
            user.reset_otp_expiry = None
            user.reset_otp_attempts = 0
        db.commit()
        return {
            "success": False,
            "message": "Invalid or expired OTP"
        }

    user.password = hash_password(reset_data.new_password)
    user.reset_otp = None
    user.reset_otp_expiry = None
    user.reset_otp_attempts = 0

    db.commit()

    return {
        "success": True,
        "message": "Password reset successfully"
    }