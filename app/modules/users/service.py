from datetime import datetime, timedelta

from sqlalchemy import String, cast, or_
from sqlalchemy.exc import IntegrityError

from app.modules.tokens.model import RefreshToken
from app.modules.users.model import User


# ======================================
# CREATE USER SERVICE
# ======================================

def create_user_service(user_data, db):

    # Check existing email
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        return {
            "success": False,
            "message": "Email already exists"
        }

    # Create new user
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        password=user_data.password,
        role=user_data.role
    )

    # Save into database
    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "id": new_user.id,
        "full_name": new_user.full_name,
        "email": new_user.email,
        "phone": new_user.phone,
        "role": new_user.role,
        "is_verified": new_user.is_verified,
        "is_active": new_user.is_active
    }


# ======================================
# GET ALL USERS SERVICE
# ======================================

def get_all_users_service(db, page=1, limit=8, search=None, role=None, status=None):

    query = db.query(User)

    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(or_(
            User.full_name.ilike(search_term),
            User.email.ilike(search_term),
            User.phone.ilike(search_term),
            cast(User.id, String).ilike(search_term),
        ))

    if role and role.lower() != "all":
        query = query.filter(User.role.ilike(role))

    if status and status.lower() != "all":
        if status.lower() == "active":
            query = query.filter(User.is_active.is_(True), User.is_verified.is_(True))
        elif status.lower() == "pending":
            query = query.filter(User.is_active.is_(True), User.is_verified.is_(False))
        elif status.lower() == "blocked":
            query = query.filter(User.is_active.is_(False))

    total = query.count()
    users = query.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    user_list = []

    for user in users:

        user_list.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
            "created_at": user.created_at
        })

    all_users = db.query(User)
    return {
        "items": user_list,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        },
        "stats": {
            "total": all_users.count(),
            "active": all_users.filter(
                User.is_active.is_(True),
                User.is_verified.is_(True)
            ).count(),
            "providers": all_users.filter(User.role.ilike("provider")).count(),
            "new_signups": all_users.filter(User.created_at >= datetime.utcnow() - timedelta(days=30)).count(),
        },
    }


# ======================================
# GET SINGLE USER SERVICE
# ======================================

def get_single_user_service(user_id, db):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "is_verified": user.is_verified,
        "is_active": user.is_active
    }


# ======================================
# UPDATE USER SERVICE
# ======================================

def update_user_service(user_id, user_data, db):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "success": False,
            "message": "User not found"
        }

    # Update fields only if provided
    if user_data.full_name is not None:
        user.full_name = user_data.full_name

    if user_data.phone is not None:
        user.phone = user_data.phone

    if user_data.profile_image is not None:
        user.profile_image = user_data.profile_image

    if user_data.role is not None:
        user.role = user_data.role

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    if user_data.is_verified is not None:
        user.is_verified = user_data.is_verified

    # Save changes
    db.commit()

    db.refresh(user)

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "profile_image": user.profile_image
    }


# ======================================
# DELETE USER SERVICE
# ======================================

def delete_user_service(user_id, db):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "success": False,
            "message": "User not found"
        }

    try:
        # Refresh tokens reference users and must be removed first.
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id
        ).delete(synchronize_session=False)

        db.delete(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        return {
            "success": False,
            "message": "User cannot be deleted because other records still reference this account."
        }

    return {
        "success": True,
        "message": f"User with ID {user_id} deleted successfully"
    }