FROM python:3.12.4-slim

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .env alembic.ini ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]