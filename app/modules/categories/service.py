from app.modules.categories.model import Category
from app.modules.services.model import Service
from sqlalchemy import or_


# ======================================
# CREATE CATEGORY SERVICE
# ======================================

def create_category_service(
    category_data,
    db
):

    existing_category = db.query(Category).filter(
        Category.name == category_data.name
    ).first()

    if existing_category:

        return {
            "success": False,
            "message": "Category already exists"
        }

    new_category = Category(
        name=category_data.name,
        description=category_data.description,
        icon=category_data.icon
    )

    db.add(new_category)

    db.commit()

    db.refresh(new_category)

    return {
        "success": True,
        "message": "Category created successfully",
        "data": new_category.to_dict()
    }


# ======================================
# GET ALL CATEGORIES
# ======================================

def get_categories_service(db, page=1, limit=8, search=None, status=None):

    query = db.query(Category)

    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.filter(or_(
            Category.name.ilike(search_term),
            Category.description.ilike(search_term),
            Category.icon.ilike(search_term),
        ))

    if status and status.lower() != "all":
        if status.lower() == "active":
            query = query.filter(Category.is_active.is_(True))
        elif status.lower() in {"inactive", "in_active"}:
            query = query.filter(Category.is_active.is_(False))

    total = query.count()
    categories = query.order_by(Category.updated_at.desc(), Category.id.desc()).offset((page - 1) * limit).limit(limit).all()

    # Convert SQLAlchemy objects to dictionaries for JSON serialization
    categories_data = [category.to_dict() for category in categories]

    return {
        "success": True,
        "data": categories_data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit,
        }
    }


def update_category_service(category_id, category_data, db):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        return {
            "success": False,
            "message": "Category not found"
        }

    duplicate = db.query(Category).filter(
        Category.name == category_data.name,
        Category.id != category_id
    ).first()

    if duplicate:
        return {
            "success": False,
            "message": "Category already exists"
        }

    category.name = category_data.name
    category.description = category_data.description
    category.icon = category_data.icon
    db.commit()
    db.refresh(category)

    return {
        "success": True,
        "message": "Category updated successfully",
        "data": category.to_dict()
    }


def delete_category_service(category_id, db):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        return {
            "success": False,
            "message": "Category not found"
        }

    service_count = db.query(Service).filter(Service.category_id == category_id).count()
    if service_count:
        return {
            "success": False,
            "message": "Category cannot be deleted while services are using it."
        }

    db.delete(category)
    db.commit()

    return {
        "success": True,
        "message": "Category deleted successfully"
    }