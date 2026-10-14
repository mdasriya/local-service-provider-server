from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database.init_db import *
from app.database.base import Base
from os import getenv
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = getenv("DATABASE_URL")
print("Database", DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base.metadata.create_all(bind=engine)

with engine.begin() as connection:
    connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR"))
    connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR"))

# ======================================
# DATABASE DEPENDENCY
# ======================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()