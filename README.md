# SHE++ API

A FastAPI backend for the SHE++ platform. The service is organized into separate layers for API routing, request/response schemas, business logic, data access, and database models.

## Core capabilities

The API is organized around these feature areas:

- Registrations and account management
- Avatars
- Games and game progress
- Organisations
- Support requests
- Administrative actions

The backend uses SQLAlchemy for database access and environment-based configuration. Its security module includes password hashing, JWT access tokens, phone-number encryption, and role-based authorization dependencies.

## Project structure

```text
.
├── app/
│   ├── core/          # Application configuration and security
│   ├── models/        # SQLAlchemy models
│   ├── repositories/  # Database access operations
│   ├── routers/       # FastAPI route definitions
│   ├── schemas/       # Request and response schemas
│   └── services/      # Business logic
├── database.py        # SQLAlchemy engine and session setup
├── main.py            # FastAPI application entry point
├── requirements.txt
└── .env.example       # Environment variable template
```

## Requirements

- Python 3.10 or newer
- PostgreSQL
- The Python packages listed in `requirements.txt`

## Local setup

1. Clone the repository and enter the project directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with `.venv\\Scripts\\Activate.ps1`.

3. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create your local environment file:

   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your local PostgreSQL connection string and strong, unique secrets. Generate a valid Fernet key for `PHONE_ENCRYPTION_KEY`; do not use the example placeholder in a running deployment.

6. Start the API from the repository root:

   ```bash
   uvicorn main:app --reload
   ```

7. Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Configuration

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy database connection URL |
| `JWT_SECRET_KEY` | Secret used to sign JWT access tokens |
| `JWT_ALGORITHM` | JWT signing algorithm (defaults to HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime |
| `PHONE_ENCRYPTION_KEY` | Fernet key used for phone-number encryption |
| `ENVIRONMENT` | Application environment |
| `DEBUG` | Debug-mode setting |

Keep real credentials in your local `.env` file or deployment secret manager. Never commit `.env` or production secrets.

## Registration and roles

Public signup is available through `POST /auth/register`. Every account created through this endpoint is assigned the `player` role by the server. The public request schema does not accept a `user_type` field, preventing callers from assigning themselves administrator or support-provider privileges. Administrator account-status changes (ban, suspend, and reactivate) are written to the admin audit log.

## Database migration

Existing PostgreSQL databases must apply the SQL migration in `migrations/20261103_add_activate_user_action.sql` before deploying the account-reactivation audit change. It adds `activate_user` to the existing `actiontype` enum used by the admin audit log.

## Tests

Run the automated tests with:

```bash
python -m unittest discover -s tests -v
```

List endpoints use validated pagination: `skip` must be zero or greater, and `limit` must be between 1 and 100.

## API documentation

When the application is running, FastAPI serves Swagger UI at `/docs` and ReDoc at `/redoc`.

## Notes

- Run the API from the repository root so application imports resolve as expected.
- Configure a PostgreSQL database before starting the service.
- The example environment file contains placeholders only; replace them with valid local configuration.
