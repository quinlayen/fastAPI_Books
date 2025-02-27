from fastapi import FastAPI, Depends, HTTPException, Path, Query
from starlette import status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, CheckConstraint, select
from pydantic import BaseModel, Field
from typing import List, Optional
from contextlib import asynccontextmanager

from database import *


# -------------------------------------------------------------------
# ORM Model Definition
# -------------------------------------------------------------------

class BookModel(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)
    published_date = Column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint('rating > 0 AND rating < 6', name='rating_range'),
        CheckConstraint('published_date > 1999 AND published_date < 2031', name='published_date_range'),
    )

# -------------------------------------------------------------------
# Pydantic Schema for Request Validation and API Documentation
# -------------------------------------------------------------------

class BookRequest(BaseModel):
    id: Optional[int] = Field(None, description="ID is not needed on create")
    title: str = Field(..., min_length=3, description="Book title (min 3 characters)")
    author: str = Field(..., min_length=1, description="Author name (min 1 character)")
    description: str = Field(..., min_length=1, max_length=100, description="Short description (1-100 characters)")
    rating: int = Field(..., gt=0, lt=6, description="Rating between 1 and 5")
    published_date: int = Field(..., gt=1999, lt=2031, description="Published year (2000-2030)")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "A new book",
                "author": "codingwithpeter",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029
            }
        }

# -------------------------------------------------------------------
# Lifespan Event to Create Tables at Startup
# -------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database tables on startup (for development purposes).
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# -------------------------------------------------------------------
# FastAPI Application Initialization
# -------------------------------------------------------------------

app = FastAPI(lifespan=lifespan)

# Dependency to get an asynchronous DB session for each request.
async def get_db():
    async with async_session() as session:
        yield session

# -------------------------------------------------------------------
# CRUD Endpoints
# -------------------------------------------------------------------

# GET: Retrieve all books.
@app.get("/books", response_model=List[BookRequest], status_code=status.HTTP_200_OK)
async def read_all_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel))
    books = result.scalars().all()
    return books

# GET: Retrieve a single book by its ID.
@app.get("/books/{book_id}", response_model=BookRequest, status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Item not found")
    return book

# GET: Retrieve books filtered by rating.
@app.get("/books/filter", response_model=List[BookRequest], status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.rating == book_rating))
    books = result.scalars().all()
    return books

# GET: Retrieve books filtered by published date.
@app.get("/books/publish", response_model=List[BookRequest], status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.published_date == published_date))
    books = result.scalars().all()
    return books

# POST: Create a new book.
@app.post("/books", response_model=BookRequest, status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest, db: AsyncSession = Depends(get_db)):
    book_data = book_request.model_dump(exclude_unset=True)
    new_book = BookModel(**book_data)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

# PUT: Update an existing book.
@app.put("/books/{book_id}", response_model=BookRequest, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_request: BookRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in book_request.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    await db.commit()
    await db.refresh(book)
    return book

# DELETE: Remove a book by its ID.
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookModel).where(BookModel.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(book)
    await db.commit()
    return None