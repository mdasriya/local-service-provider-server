from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ================================
# BASE SCHEMA
# ================================

class UserBaseSchema(BaseModel):

    full_name: str = Field(
        min_length=3,
        max_length=100,
        example="Mukesh Dasriya"
    )

    email: EmailStr

    phone: str = Field(
        min_length=10,
        max_length=15,
        example="9876543210"
    )


# ================================
# CREATE USER SCHEMA
# ================================

class UserCreateSchema(UserBaseSchema):

    password: str = Field(
        min_length=6,
        max_length=50,
        example="mypassword123"
    )

    role: str = Field(
        default="customer",
        example="customer"
    )


# ================================
# UPDATE USER SCHEMA
# ================================

class UserUpdateSchema(BaseModel):

    full_name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    phone: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15
    )

    profile_image: Optional[str] = None

    role: Optional[str] = None

    is_active: Optional[bool] = None

    is_verified: Optional[bool] = None


# ================================
# RESPONSE SCHEMA
# ================================

class UserResponseSchema(UserBaseSchema):

    id: int

    role: str

    profile_image: Optional[str] = None

    is_verified: bool

    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    email: EmailStr
    otp: str
    new_password: str