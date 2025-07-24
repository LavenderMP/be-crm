# Event Management CRM - FastAPI Backend

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-100000?style=for-the-badge)

A high-performance backend system for event management platforms, featuring user CRM, event registration, and email campaign capabilities. Built with FastAPI and PostgreSQL for scalability and maintainability.

## Features

- **User Management**
  - Create and manage user profiles
  - Advanced filtering (company, location, job title)
  - Pagination and sorting
- **Event Management**
  - Create and manage events
  - Track attendance and hosting history
- **Email Campaigns**
  - Send targeted emails based on filters
  - Track campaign status and analytics
- **Performance**
  - Optimized queries for large datasets
  - Background task processing
  - Scalable architecture

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Testing**: Pytest, SQLite (in-memory)
- **Deployment**: Docker-ready

## Installation

```
docker-compose up --build
```

## Migrate data

```
alembic upgrade head
```

- then reload docker

## Generate fake data for testing

```
curl -X 'GET' \
  'http://0.0.0.0:8000/gen-fake-data' \
  -H 'accept: application/json'
```

## API Documentation

Interactive documentation available at:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Example Requests

```
1. curl -X GET "http://localhost:8000/users?company=Google&state=CA&hosted_events_min=3&page=1&size=5"
2. curl -X POST "http://localhost:8000/event/send_emails" \
-H "Content-Type: application/json" \
-d '{"filters": {"company": "Microsoft", "state": "WA"}, "subject": "New Event", "body": "Content"}'
```

## Testing

**Key Testing Features:**
  - Comprehensive Coverage:
  - Core CRUD operations
  - Filtering and pagination

