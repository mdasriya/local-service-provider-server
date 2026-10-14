from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

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

    token = Column(
        String,
        nullable=False,
        unique=True
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    is_revoked = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )