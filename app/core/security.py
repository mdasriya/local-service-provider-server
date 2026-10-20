from passlib.context import CryptContext
import hashlib
import os

from jose import jwt, JWTError

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is required. Set it in the backend .env file."
    )

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)


# ======================================
# HASH PASSWORD
# ======================================

def hash_password(password: str):
    # Pre-hash the raw password with SHA-256 and hash the hex digest with bcrypt.
    # This avoids bcrypt's 72-byte limit while keeping stored hashes compatible
    # with bcrypt verification via the same transform.
    return pwd_context.hash(password)


# ======================================
# VERIFY PASSWORD
# ======================================

def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(plain_password, hashed_password)


# ======================================
# CREATE ACCESS TOKEN
# ======================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ======================================
# VERIFY ACCESS TOKEN
# ======================================

def verify_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


# ======================================
# CREATE REFRESH TOKEN
# ======================================

def create_refresh_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({
        "exp": expire,
        "token_type": "refresh"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ======================================
# VERIFY REFRESH TOKEN
# ======================================

def verify_refresh_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("token_type") != "refresh":

            return None

        return payload

    except JWTError:

        return None