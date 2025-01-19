FROM python:3.11-slim

WORKDIR /api

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --host $API_HOST --port $API_PORT"]

