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

3. Set up your environment variables as described in the "Environment Variables" section below.

4. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

5. The application will be available at `http://localhost:8000`

6. Access the API documentation at `http://localhost:8000/docs`

## Environment Variables

To run this project, you need to set up the following environment variables:

1. Copy the `.env.example` file to a new file named `.env`:

   ```
   cp .env.example .env
   ```

2. Open the `.env` file and update the values:

   - `DATABASE_URL`: This should match the URL in your `docker-compose.yml` file. The default value should work if you haven't changed the database configuration.
   - `GROK_API_KEY`: Replace `your_grok_api_key_here` with your actual Grok API key.

3. Make sure not to commit your `.env` file to version control. It should be listed in your `.gitignore` file.

## Usage

Use the API endpoints to manage books, add reviews, generate summaries, and get recommendations.
