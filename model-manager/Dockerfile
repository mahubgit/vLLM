FROM python:3.9-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Create necessary directories
RUN mkdir -p app/static

COPY app/ app/
WORKDIR /app
ENV PYTHONPATH=/app

CMD ["python", "main.py"]