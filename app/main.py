
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.routes import (router as auth_router)
from app.modules.providers.routes import (router as provider_router)
from app.modules.categories.routes import (router as category_router)
from app.database.base import Base
from app.database.session import engine
from app.modules.services.model import Service
from app.modules.services.routes import (
    router as service_router
)
from app.modules.bookings.model import Booking

from app.modules.bookings.routes import (
    router as booking_router
)
from app.modules.reviews.model import Review

from app.modules.reviews.routes import (
    router as review_router
)
from app.modules.availability.routes import (
    router as availability_router
)
from app.modules.customers.routes import (
    router as customer_router
)
from app.modules.notifications.routes import (
    router as notification_router
)
from app.modules.favorites.routes import (
    router as favorite_router
)
from app.modules.password.routes import (
    router as password_router
)
from app.modules.chat.routes import (
    router as chat_router
)



from app.modules.users.model import User
from app.modules.users.routes import router as user_router
from app.modules.admin.routes import router as admin_router
from app.modules.tokens.routes import router as token_router


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

local_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]
configured_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
# postgresql://neondb_owner:npg_bEtcV0xW7Mhy@ep-wild-shadow-b5r8tf4b-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*local_origins, *configured_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(provider_router) 
app.include_router(category_router)
app.include_router(service_router)
app.include_router(booking_router)
app.include_router(review_router)
app.include_router(admin_router)
app.include_router(availability_router)
app.include_router(customer_router)
app.include_router(token_router)
app.include_router(notification_router)
app.include_router(favorite_router)
app.include_router(password_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "ServiceHub Backend Running"
    }