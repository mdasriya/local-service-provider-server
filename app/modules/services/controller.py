from app.modules.services.service import (
    create_service_service,
    get_services_service,
    search_services_service,
    create_service_for_provider_service
)


# ======================================
# CREATE SERVICE CONTROLLER
# ======================================

def create_service_controller(
    service_data,
    current_user,
    db
):

    return create_service_service(
        service_data,
        current_user,
        db
    )


# ======================================
# GET SERVICES CONTROLLER
# ======================================

def get_services_controller(db, page=1, limit=8, search=None, category_id=None, status=None):

    return get_services_service(db, page, limit, search, category_id, status)


# ======================================
# SEARCH SERVICES
# ======================================

def search_services_controller(

    db,

    keyword=None,

    category_id=None,

    min_price=None,

    max_price=None,

    sort_by=None,

    page=1,

    limit=10
):

    return search_services_service(
        db,
        keyword,
        category_id,
        min_price,
        max_price,
        sort_by,
        page,
        limit
    )


def create_admin_service_controller(service_data, db):

    return create_service_for_provider_service(service_data, service_data.provider_id, db)