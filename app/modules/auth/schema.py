from pydantic import BaseModel, EmailStr


# ======================================
# REGISTER SCHEMA
# ======================================

class RegisterSchema(BaseModel):

    email: EmailStr

    password: str

    role: str = "customer"


# ======================================
# LOGIN SCHEMA
# ======================================

class LoginSchema(BaseModel):

    email: EmailStr

    password: str