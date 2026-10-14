from pydantic import BaseModel
from datetime import time


# ======================================
# CREATE AVAILABILITY SCHEMA
# ======================================

class AvailabilityCreateSchema(BaseModel):

    day: str

    start_time: time

    end_time: time


# ======================================
# RESPONSE SCHEMA
# ======================================

class AvailabilityResponseSchema(BaseModel):

    id: int

    provider_id: int

    day: str

    start_time: time

    end_time: time

    is_available: bool

    class Config:

        from_attributes = True