from pydantic import BaseModel
from typing import Optional


# ======================================
# CREATE REVIEW
# ======================================

class ReviewCreateSchema(BaseModel):

    booking_id: int

    rating: int

    comment: Optional[str] = None