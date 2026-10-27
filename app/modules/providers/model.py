from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DateTime,
    DECIMAL
)

from sqlalchemy.sql import func

from app.database.base import Base



class Provider(Base):

    __tablename__ = "providers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    bio = Column(
        Text,
        nullable=True
    )

    experience = Column(
        Integer,
        default=0
    )

    service_area = Column(
        String,
        nullable=True
    )

    hourly_rate = Column(
        DECIMAL,
        nullable=True
    )

    average_rating = Column(
        DECIMAL,
        default=0
    )

    total_reviews = Column(
        Integer,
        default=0
    )

    government_id = Column(
        String,
        nullable=True
    )

    verification_status = Column(
        String,
        default="pending"
    )
    average_rating = Column(
    DECIMAL,
    default=0
    )

    total_reviews = Column(
    Integer,
    default=0
    )
    image = Column(String, nullable=True)
    provider_type = Column(String, nullable=True)
    category = Column(String, nullable=True)
    city = Column(String, nullable=True)
    locality = Column(String, nullable=True)
    service_radius = Column(Integer, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )
