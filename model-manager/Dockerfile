FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .
RUN mkdir -p templates
COPY app/templates/ templates/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]