from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models, schemas

async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(
        select(models.Book).options(selectinload(models.Book.reviews)).filter(models.Book.id == book_id)
    )
    return result.scalars().first()

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Book).offset(skip).limit(limit))
    return result.scalars().all()

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookCreate):
    db_book = await get_book(db, book_id)
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        await db.commit()
        await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
    return db_book

async def create_review(db: AsyncSession, review: schemas.ReviewCreate, book_id: int):
    db_review = models.Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_reviews(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Review).filter(models.Review.book_id == book_id))
    return result.scalars().all()