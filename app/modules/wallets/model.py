from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime

from app.database.base import Base


class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    provider_id = Column(
        Integer,
        ForeignKey("providers.id")
    )

    balance = Column(
        Float,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )