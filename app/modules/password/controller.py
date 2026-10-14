from app.modules.password.service import (
    forgot_password_service,
    reset_password_service
)


# ======================================
# FORGOT PASSWORD CONTROLLER
# ======================================

def forgot_password_controller(
    forgot_data,
    db
):

    return forgot_password_service(
        forgot_data,
        db
    )


# ======================================
# RESET PASSWORD CONTROLLER
# ======================================

def reset_password_controller(
    reset_data,
    db
):

    return reset_password_service(
        reset_data,
        db
    )