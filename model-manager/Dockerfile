FROM python:3.9-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Create necessary directories
RUN mkdir -p static

# Copy the application files correctly
COPY app/. .

# Create health endpoint file
RUN echo '{"status": "ok"}' > static/health.json

# Set the working directory
WORKDIR /app

CMD ["python", "main.py"]