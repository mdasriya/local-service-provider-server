from app.modules.tokens.service import (
    refresh_access_token_service,
    logout_service
)


# ======================================
# REFRESH ACCESS TOKEN CONTROLLER
# ======================================

def refresh_access_token_controller(
    refresh_token_data,
    db
):

    return refresh_access_token_service(
        refresh_token_data,
        db
    )


# ======================================
# LOGOUT CONTROLLER
# ======================================

def logout_controller(
    refresh_token_data,
    db
):

    return logout_service(
        refresh_token_data,
        db
    )