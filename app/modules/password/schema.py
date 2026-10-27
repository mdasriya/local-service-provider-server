from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordSchema(BaseModel):

    email: EmailStr


class ResetPasswordSchema(BaseModel):

    email: EmailStr

    otp: str = Field(min_length=6, max_length=6, pattern=r"^[0-9]{6}$")

    new_password: str = Field(min_length=8, max_length=128)