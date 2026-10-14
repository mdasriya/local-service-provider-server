from sqlalchemy import and_, or_, cast, String

from app.modules.providers.model import Provider

from app.modules.categories.model import Category
from sqlalchemy import and_
from app.modules.services.model import Service
from app.modules.users.model import User


# ======================================
# CREATE SERVICE
# ======================================

def create_service_service(
    service_data,
    current_user,
    db
):

    provider = db.query(Provider).filter(
        Provider.user_id == current_user.id
    ).first()

    if not provider:

        return {
            "success": False,
            "message": "Provider profile not found"
        }

    return create_service_for_provider_service(service_data, provider.id, db)


def create_service_for_provider_service(service_data, provider_id, db):

    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        return {"success": False, "message": "Provider not found"}

    category = db.query(Category).filter(
        Category.id == service_data.category_id
    ).first()

    if not category:

        return {
            "success": False,
            "message": "Category not found"
        }

    # ======================================
    # CREATE SERVICE
    # ======================================

    new_service = Service(

        provider_id=provider_id,

        category_id=service_data.category_id,

        title=service_data.title,

        description=service_data.description,

        price=getattr(service_data, "price", 0),

        duration_minutes=getattr(service_data, "duration_minutes", 0),

        image=service_data.image
    )

    db.add(new_service)

    db.commit()

    db.refresh(new_service)

    return {
        "success": True,
        "message": "Service created successfully",
        "data": {
            "id": new_service.id,
            "title": new_service.title,
            "price": float(new_service.price)
        }
    }


# ======================================
# GET ALL SERVICES
# ======================================

def get_services_service(db, page=1, limit=8, search=None, category_id=None, status=None):

    query = db.query(Service, Category, Provider, User).join(
        Category, Service.category_id == Category.id
    ).join(
        Provider, Service.provider_id == Provider.id
    ).join(
        User, Provider.user_id == User.id
    )

    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.filter(or_(
            Service.title.ilike(search_term),
            Category.name.ilike(search_term),
            User.full_name.ilike(search_term),
            User.email.ilike(search_term),
            cast(Service.id, String).ilike(search_term),
        ))

    if category_id and category_id != "all":
        query = query.filter(Service.category_id == int(category_id))

    if status and status.lower() != "all":
        query = query.filter(Service.is_active.is_(status.lower() == "active"))

    total = query.count()
    service_rows = query.order_by(Service.updated_at.desc(), Service.id.desc()).offset((page - 1) * limit).limit(limit).all()

    services_data = [{
        "id": service.id,
        "title": service.title,
        "description": service.description,
        "price": float(service.price),
        "is_active": service.is_active,
        "updated_at": service.updated_at,
        "category_id": category.id,
        "category_name": category.name,
        "category_icon": category.icon,
        "provider_name": user.full_name or user.email,
        "provider_email": user.email,
    } for service, category, provider, user in service_rows]

    return {
        "success": True,
        "data": services_data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        }
    }


# ======================================
# SEARCH SERVICES
# ======================================

def search_services_service(

    db,

    keyword=None,

    category_id=None,

    min_price=None,

    max_price=None,

    sort_by=None,

    page=1,

    limit=10
):

    query = db.query(Service)

    # ======================================
    # SEARCH KEYWORD
    # ======================================

    if keyword:

        query = query.filter(
            Service.title.ilike(f"%{keyword}%")
        )

    # ======================================
    # CATEGORY FILTER
    # ======================================

    if category_id:

        query = query.filter(
            Service.category_id == category_id
        )

    # ======================================
    # MIN PRICE
    # ======================================

    if min_price is not None:

        query = query.filter(
            Service.price >= min_price
        )

    # ======================================
    # MAX PRICE
    # ======================================

    if max_price is not None:

        query = query.filter(
            Service.price <= max_price
        )

    # ======================================
    # ACTIVE SERVICES
    # ======================================

    query = query.filter(
        Service.is_active == True
    )

    # ======================================
    # SORTING
    # ======================================

    if sort_by == "price_low":

        query = query.order_by(
            Service.price.asc()
        )

    elif sort_by == "price_high":

        query = query.order_by(
            Service.price.desc()
        )

    elif sort_by == "newest":

        query = query.order_by(
            Service.created_at.desc()
        )

    # ======================================
    # PAGINATION
    # ======================================

    offset = (page - 1) * limit

    services = query.offset(offset).limit(limit).all()

    total = query.count()

    return {
        "success": True,
        "page": page,
        "limit": limit,
        "total": total,
        "data": services
    }