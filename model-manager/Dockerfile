FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .
# Create static directory
RUN mkdir -p static

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]