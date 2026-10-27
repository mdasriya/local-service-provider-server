from pydantic import BaseModel
from typing import Optional


# ======================================
# CREATE PROVIDER SCHEMA
# ======================================

class ProviderCreateSchema(BaseModel):

    bio: Optional[str] = None

    experience: int

    service_area: str

    hourly_rate: Optional[float] = None

    government_id: Optional[str] = None

    image: str | None = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    provider_type: Optional[str] = None
    category: Optional[str] = None
    city: Optional[str] = None
    locality: Optional[str] = None
    service_radius: Optional[int] = None


class AdminProviderCreateSchema(ProviderCreateSchema):

    user_id: int


class AdminProviderUpdateSchema(BaseModel):

    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    experience: Optional[int] = None
    service_area: Optional[str] = None
    hourly_rate: Optional[float] = None
    government_id: Optional[str] = None
    verification_status: Optional[str] = None
    is_active: Optional[bool] = None
    image: Optional[str] = None