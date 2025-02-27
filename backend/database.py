from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------------------
# Database Connection Configuration using psycopg (psycopg 3)
# -------------------------------------------------------------------

# Use the new psycopg driver by specifying "postgresql+psycopg" in the connection string.
DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/booksdb"

# Create an asynchronous engine using psycopg.
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker that produces asynchronous sessions.
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Create a declarative base class for ORM models.
Base = declarative_base()