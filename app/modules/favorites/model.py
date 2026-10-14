from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime
)

from datetime import datetime, timezone

from app.database.base import Base


class Favorite(Base):

    __tablename__ = "favorites"

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

    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )