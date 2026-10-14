from app.modules.categories.service import (
    create_category_service,
    get_categories_service,
    update_category_service,
    delete_category_service
)


# ======================================
# CREATE CATEGORY CONTROLLER
# ======================================

def create_category_controller(
    category_data,
    db
):

    return create_category_service(
        category_data,
        db
    )


# ======================================
# GET CATEGORIES CONTROLLER
# ======================================

def get_categories_controller(db, page=1, limit=8, search=None, status=None):

    return get_categories_service(db, page, limit, search, status)


def update_category_controller(category_id, category_data, db):

    return update_category_service(category_id, category_data, db)


def delete_category_controller(category_id, db):

    return delete_category_service(category_id, db)