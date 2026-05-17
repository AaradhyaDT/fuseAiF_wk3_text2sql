# Dockerfile for Text-to-SQL Agentic System
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# copy requirements first to leverage cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application
COPY . .

EXPOSE 8000

# default environment variables (overridable by docker-compose / env file)
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=classicmodels
ENV DB_USER=postgres
ENV DB_PASSWORD=password

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
