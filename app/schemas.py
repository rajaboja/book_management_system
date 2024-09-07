from pydantic import BaseModel
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    summary: Optional[str] = None

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int

    class Config:
        orm_mode = True

class BookWithReviews(Book):
    reviews: List[Review] = []

class RecommendationRequest(BaseModel):
    user_id: int
    preferred_genres: List[str]