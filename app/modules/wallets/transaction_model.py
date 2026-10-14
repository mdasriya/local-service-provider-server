from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    provider_id = Column(
        Integer,
        ForeignKey("providers.id")
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id")
    )

    amount = Column(
        Float
    )

    commission = Column(
        Float
    )

    provider_earning = Column(
        Float
    )

    status = Column(
        String,
        default="completed"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )