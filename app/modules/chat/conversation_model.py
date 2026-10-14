from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime, timezone

from app.database.base import Base


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
        unique=True
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

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )