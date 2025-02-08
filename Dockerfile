FROM --platform=linux/arm64 python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENV FLASK_APP=src.app:application
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]