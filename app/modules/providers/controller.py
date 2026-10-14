from app.modules.providers.service import (
    create_provider_service,
    get_top_providers_service,
    get_providers_service,
    create_provider_for_user_service,
    update_provider_service,
)


# ======================================
# CREATE PROVIDER CONTROLLER
# ======================================

def create_provider_controller(
    provider_data,
    current_user,
    db
):

    return create_provider_service(
        provider_data,
        current_user,
        db
    )


def create_admin_provider_controller(provider_data, db):

    return create_provider_for_user_service(provider_data, provider_data.user_id, db)


def update_provider_controller(provider_id, provider_data, db):

    return update_provider_service(provider_id, provider_data, db)

# ======================================
# GET TOP PROVIDERS
# ======================================

def get_top_providers_controller(db):

    return get_top_providers_service(db)


def get_providers_controller(db, page=1, limit=8, search=None, verification_status=None, status=None):

    return get_providers_service(db, page, limit, search, verification_status, status)

