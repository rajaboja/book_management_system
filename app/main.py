from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, models, schemas, database, ai_integration, recommendation
from typing import List

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with database.AsyncSessionLocal() as session:
        books = await crud.get_books(session)
        recommendation.recommendation_system.fit(books)

@app.post("/books/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.create_book(db, book)
    # Update recommendation system when a new book is added
    async with database.AsyncSessionLocal() as session:
        books = await crud.get_books(session)
        recommendation.recommendation_system.fit(books)
    return db_book

@app.get("/books/", response_model=List[schemas.Book])
async def read_books(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)):
    books = await crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.BookWithReviews)
async def read_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return schemas.BookWithReviews(
        id=db_book.id,
        title=db_book.title,
        author=db_book.author,
        genre=db_book.genre,
        year_published=db_book.year_published,
        summary=db_book.summary,
        reviews=[schemas.Review.from_orm(review) for review in db_book.reviews]
    )

@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookCreate, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.update_book(db, book_id, book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", response_model=schemas.Book)
async def delete_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books/{book_id}/reviews/", response_model=schemas.Review)
async def create_review(book_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_review(db, review, book_id)

@app.get("/books/{book_id}/reviews/", response_model=List[schemas.Review])
async def read_reviews(book_id: int, db: AsyncSession = Depends(database.get_db)):
    reviews = await crud.get_reviews(db, book_id)
    return reviews

@app.get("/books/{book_id}/summary/")
async def get_book_summary(book_id: int, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if not db_book.summary:
        # Generate summary using Llama 3
        book_content = f"{db_book.title} by {db_book.author}. Genre: {db_book.genre}. Published in {db_book.year_published}."
        db_book.summary = await ai_integration.llama_integration.generate_summary(book_content)
        await crud.update_book(db, book_id, schemas.BookCreate(**db_book.__dict__))
    
    reviews = await crud.get_reviews(db, book_id)
    avg_rating = sum(review.rating for review in reviews) / len(reviews) if reviews else None
    
    return {"summary": db_book.summary, "average_rating": avg_rating}

@app.post("/recommendations/", response_model=List[schemas.Book])
async def get_recommendations(request: schemas.RecommendationRequest):
    recommendations = recommendation.recommendation_system.get_recommendations(request.preferred_genres)
    return recommendations

@app.post("/generate-summary/")
async def generate_summary(book_content: str):
    summary = await ai_integration.llama_integration.generate_summary(book_content)
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)