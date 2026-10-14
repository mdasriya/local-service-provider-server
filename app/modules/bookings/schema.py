from pydantic import BaseModel
from datetime import date, time


# ======================================
# CREATE BOOKING
# ======================================

class BookingCreateSchema(BaseModel):

    service_id: int

    booking_date: date

    booking_time: time

    address: str