from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database.base import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

  
    email = Column(String, unique=True, nullable=False)

    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    password = Column(String, nullable=False)

    role = Column(String, default="customer")

    profile_image = Column(String, nullable=True)
    reset_otp = Column(String, nullable=True)
    reset_otp_expiry = Column(DateTime, nullable=True)

    is_verified = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)
    
    reset_token = Column(
    String,
    nullable=True
    )

    reset_token_expiry = Column(
    DateTime,
    nullable=True
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )