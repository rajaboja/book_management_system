from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommendationSystem:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.book_vectors = None
        self.books = []

    def fit(self, books):
        self.books = books
        if not books:
            print("No books available for recommendation system.")
            return
        book_features = [f"{book.genre} {book.title} {book.author}" for book in books]
        self.book_vectors = self.vectorizer.fit_transform(book_features)

    def get_recommendations(self, user_preferences, top_n=5):
        if not self.books:
            return []
        user_vector = self.vectorizer.transform([" ".join(user_preferences)])
        similarities = cosine_similarity(user_vector, self.book_vectors)
        top_indices = np.argsort(similarities[0])[::-1][:top_n]
        return [self.books[i] for i in top_indices]

recommendation_system = RecommendationSystem()