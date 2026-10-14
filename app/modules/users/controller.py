from app.modules.users.service import (
    create_user_service,
    get_all_users_service,
    get_single_user_service,
    update_user_service,
    delete_user_service
)


# ======================================
# CREATE USER CONTROLLER
# ======================================

def create_user_controller(user_data, db):

    user = create_user_service(user_data, db)

    if user.get("success") is False:
        return user

    return {
        "success": True,
        "message": "User created successfully",
        "data": user
    }


# ======================================
# GET ALL USERS CONTROLLER
# ======================================

def get_all_users_controller(db, page=1, limit=8, search=None, role=None, status=None):

    users = get_all_users_service(db, page, limit, search, role, status)

    return {
        "success": True,
        "message": "Users fetched successfully",
        "data": users["items"],
        "pagination": users["pagination"],
        "stats": users["stats"]
    }


# ======================================
# GET SINGLE USER CONTROLLER
# ======================================

def get_single_user_controller(user_id, db):

    user = get_single_user_service(user_id, db)

    return {
        "success": True,
        "message": "User fetched successfully",
        "data": user
    }

# ======================================
# UPDATE USER CONTROLLER
# ======================================

def update_user_controller(user_id, user_data, db):

    updated_user = update_user_service(
        user_id,
        user_data,
        db
    )

    return {
        "success": True,
        "message": "User updated successfully",
        "data": updated_user
    }


# ======================================
# DELETE USER CONTROLLER
# ======================================

def delete_user_controller(user_id, db):

    result = delete_user_service(user_id, db)

    return result