FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create tables before starting the application
CMD python create_tables.py && uvicorn app.main:app --host 0.0.0.0 --port 8000