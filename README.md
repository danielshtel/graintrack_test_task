# Installation guide

## Clone the project
```bash
git clone https://github.com/danielshtel/graintrack_test_task.git
```
## Cook the env variables
```bash
cd graintrack_test_task
cp .env.example
```

## Start containers
```bash
docker compose up --build -d
```

## Upload DB dump
```bash
docker-compose exec -T db psql -U graintrack graintrack < dump.sql
```

## Usage:
* API docs are available on [Swagger Docs](http://localhost:8000/docs).
* Application use JWT authentication
* You can use standard admin credentials
```
username: admin
password: admin123!
```
* Or you can create your own simple user via /sign-up endpoint
* Endpoints which require admin rights are documented


## Tech stack:
- FastAPI, Pydantic, SQLAlchemy, PostgreSQL, Alembic