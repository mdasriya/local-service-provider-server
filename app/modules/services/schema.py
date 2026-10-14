from pydantic import BaseModel
from typing import Optional


# ======================================
# CREATE SERVICE SCHEMA
# ======================================

class ServiceCreateSchema(BaseModel):

    category_id: int

    title: str

    description: Optional[str] = None

    price: float

    duration_minutes: int
    
    image: str | None = None


class AdminServiceCreateSchema(BaseModel):

    provider_id: int

    category_id: int

    title: str

    description: Optional[str] = None

    image: str | None = None