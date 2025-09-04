# docker/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app  
    # <- lets Python import "src.*"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# copy project (your compose already builds with context=../)
COPY . .
