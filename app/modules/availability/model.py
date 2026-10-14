from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Time,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class Availability(Base):

    __tablename__ = "provider_availability"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    provider_id = Column(
        Integer,
        ForeignKey("providers.id"),
        nullable=False
    )

    day = Column(
        String,
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    is_available = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )