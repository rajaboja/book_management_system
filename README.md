# Intelligent Book Management System

This project implements an intelligent book management system using Python, FastAPI, PostgreSQL, and the Llama 3 generative AI model provided by Groq.

## Features

- Book management (CRUD operations)
- Review system
- AI-generated book summaries
- Book recommendations based on user preferences
- Asynchronous database operations

## Running with Docker

1. Make sure you have Docker and Docker Compose installed on your system.

2. Clone this repository:
   ```
   git clone https://github.com/yourusername/book-management-system.git
   cd book-management-system
   ```

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. The application will be available at `http://localhost:8000`

5. Access the API documentation at `http://localhost:8000/docs`

## Usage

Use the API endpoints to manage books, add reviews, generate summaries, and get recommendations.
