from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin_or_local_development

from app.database.session import get_db

from app.modules.users.schema import UserCreateSchema, UserUpdateSchema

from app.modules.users.controller import (
    create_user_controller,
    get_all_users_controller,
    get_single_user_controller,
    delete_user_controller,
    update_user_controller
   
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ======================================
# CREATE USER
# ======================================

@router.post("/")
def create_user(
    user: UserCreateSchema,
    db: Session = Depends(get_db)
):

    return create_user_controller(user, db)


# ======================================
# GET ALL USERS
# ======================================

@router.get("/")
def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(8, ge=1, le=100),
    search: str | None = Query(None),
    role: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db)
):

    return get_all_users_controller(db, page, limit, search, role, status)


# ======================================
# GET SINGLE USER
# ======================================

@router.get("/{user_id}", dependencies=[Depends(require_admin_or_local_development)])
def get_single_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return get_single_user_controller(user_id, db)

# ======================================
# UPDATE USER
# ======================================

@router.put("/{user_id}", dependencies=[Depends(require_admin_or_local_development)])
def update_user(
    user_id: int,
    user: UserUpdateSchema,
    db: Session = Depends(get_db)
):

    return update_user_controller(
        user_id,
        user,
        db
    )


# ======================================
# DELETE USER
# ======================================

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return delete_user_controller(user_id, db)
