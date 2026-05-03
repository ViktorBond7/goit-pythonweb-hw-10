# Contact Book API

REST API for managing contacts with user authentication, email confirmation, avatar upload, birthday reminders, and rate limiting.

## Features

- User registration and login with JWT tokens
- Refresh token flow
- Email confirmation
- User profile endpoint
- Avatar upload with Cloudinary
- CRUD for contacts
- Search contacts by `first_name`, `last_name`, or `email`
- Upcoming birthdays for the next 7 days
- Rate limiting with SlowAPI
- Async SQLAlchemy + PostgreSQL
- Alembic migrations
- Docker support

## Tech stack

- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Alembic
- Poetry
- SlowAPI
- FastAPI-Mail
- Cloudinary

## Project structure

- `main.py` — application entry point
- `src/api/` — API routes
- `src/services/` — business logic
- `src/repositories/` — database access layer
- `src/models/` — SQLAlchemy models
- `src/schemas/` — Pydantic schemas
- `src/db/` — async database session
- `alembic/` — migrations
- `docker-compose.yml` — app + PostgreSQL services
- `Dockerfile` — container image for API

## Environment variables

Create a `.env` file in the project root.

Required variables:

```env
DATABASE_CONNECT_URL=postgresql+asyncpg://admin:password@localhost:5433/db_contacts
SECRET_KEY=your_secret_key
ALGORITHM=HS256

POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=db_contacts

MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_PORT=465
MAIL_SERVER=smtp.example.com

CLD_NAME=your_cloudinary_name
CLD_API_KEY=your_cloudinary_api_key
CLD_API_SECRET=your_cloudinary_api_secret
```

## Run locally

### 1. Install dependencies

```bash
poetry install
```

### 2. Start PostgreSQL

```bash
docker-compose up -d postgres
```

### 3. Apply migrations

```bash
poetry run alembic upgrade head
```

### 4. Start the API

```bash
poetry run fastapi dev main.py
```

API will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Run with Docker Compose

```bash
docker-compose up -d --build
```

Services:

- API: `http://127.0.0.1:8000`
- PostgreSQL: host port `5433`

After containers start, run migrations if needed:

```bash
poetry run alembic upgrade head
```

## Database migrations

Create a migration:

```bash
poetry run alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
poetry run alembic upgrade head
```

## Main endpoints

### Auth and users

- `POST /register` — register user
- `POST /login` — login user
- `GET /me` — current authenticated user
- `GET /confirmed_email/{token}` — confirm email
- `POST /request_email` — resend confirmation email
- `POST /refresh` — refresh access token
- `PATCH /avatar` — upload/update avatar

### Contacts

- `GET /contacts/` — list contacts
- `POST /contacts/` — create contact
- `GET /contacts/{contact_id}` — get contact by id
- `PATCH /contacts/{contact_id}` — update contact
- `DELETE /contacts/{contact_id}` — delete contact
- `GET /contacts/birthdays/upcoming` — contacts with birthdays in next 7 days

### Search contacts

Use query parameters on `GET /contacts/`:

- `first_name`
- `last_name`
- `email`

Example:

```http
GET /contacts/?first_name=ivan&email=gmail.com
```

## Authentication

Protected endpoints require Bearer token:

```http
Authorization: Bearer <access_token>
```

## Notes

- `/me` is rate-limited.
- CORS is enabled in the application.
- Email and avatar features require valid external service credentials.

## Author

ViktorBond7
