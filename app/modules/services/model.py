from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    DateTime,
    DECIMAL
)

from sqlalchemy.sql import func

from app.database.base import Base


class Service(Base):

    __tablename__ = "services"

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

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    price = Column(
        DECIMAL,
        nullable=False
    )

    duration_minutes = Column(
        Integer,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )
    image = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )