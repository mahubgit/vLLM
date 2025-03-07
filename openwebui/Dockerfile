FROM python:3.9-slim

RUN pip install gradio requests openai

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]