FROM python:3.12-slim

WORKDIR /app

COPY .env /app

COPY src/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \

COPY src/ /app
