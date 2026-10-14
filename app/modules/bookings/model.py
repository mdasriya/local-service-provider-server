from sqlalchemy import (Column,Integer,String,ForeignKey,DateTime,DECIMAL)
from sqlalchemy.sql import func
from app.database.base import Base
from sqlalchemy import Date, Time

class Booking(Base):

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    provider_id = Column(
        Integer,
        ForeignKey("providers.id"),
        nullable=False
    )

    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
    )

    booking_date = Column(
        String,
        nullable=False
    )

    booking_time = Column(
        String,
        nullable=False
    )

    address = Column(
        String,
        nullable=False
    )

    total_price = Column(
        DECIMAL,
        nullable=False
    )

    status = Column(
        String,
        default="pending"
    )
    booking_date = Column(
    Date,
    nullable=False
    )

    booking_time = Column(
    Time,
    nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )