# FastAPI Blog API

A REST API project for learning and implementing production-style backend concepts with FastAPI, PostgreSQL, SQLAlchemy, and Pydantic.

[View repository](https://github.com/talha-amr/fastapi-blog-api)

## Current capabilities

- Create, retrieve, update, and delete posts
- Retrieve the latest post
- Create users with hashed passwords
- Validate login credentials
- PostgreSQL persistence through SQLAlchemy
- Pydantic request and response validation
- Router-based FastAPI project structure
- Automatic interactive API documentation

## Authentication status

Password hashing and credential validation are implemented. Token generation and protected-route authorization are currently in progress; the login route should not yet be treated as production-ready authentication.

## Built with

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Psycopg 3
- Pydantic
- Passlib and bcrypt
- Uvicorn

## Run locally

### Prerequisites

- Python 3.11 or newer
- PostgreSQL

### Installation

```bash
git clone https://github.com/talha-amr/fastapi-blog-api.git
cd fastapi-blog-api
python -m venv venv
```

Activate the environment:

```powershell
venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
```

Start the server:

```bash
uvicorn app.main:app --reload
```

## API documentation

After starting the server:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Main endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/posts/` | Retrieve all posts |
| GET | `/posts/latest` | Retrieve the newest post |
| GET | `/posts/{id}` | Retrieve one post |
| POST | `/posts/` | Create a post |
| PUT | `/posts/{id}` | Replace a post |
| DELETE | `/posts/{id}` | Delete a post |
| POST | `/users` | Create a user |
| POST | `/login` | Validate credentials |

## Next steps

- Generate signed JWT access tokens
- Protect user-specific routes
- Associate posts with their owners
- Add Alembic database migrations
- Add automated API tests

## Author

**Muhamad Talha Amir** — [GitHub](https://github.com/talha-amr)
