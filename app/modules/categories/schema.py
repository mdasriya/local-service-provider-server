from pydantic import BaseModel
from typing import Optional


# ======================================
# CREATE CATEGORY SCHEMA
# ======================================

class CategoryCreateSchema(BaseModel):

    name: str

    description: Optional[str] = None

    icon: Optional[str] = None


class CategoryUpdateSchema(BaseModel):

    name: str

    description: Optional[str] = None

    icon: Optional[str] = None

    is_active: Optional[bool] = None