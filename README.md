# Licitações API

REST API for managing public procurement records, built with FastAPI, PostgreSQL and SQLAlchemy.

The project was developed with a focus on backend fundamentals such as RESTful design, data validation, persistence, database migrations, filtering, pagination, automated tests and containerized execution.

## Tech Stack

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Pydantic
- Alembic
- Psycopg 3
- Pytest
- Docker
- Docker Compose

## Features

- Create procurement records
- List procurement records
- Retrieve a procurement record by ID
- Update existing records
- Delete records
- Filter by city
- Filter by procurement modality
- Case-insensitive partial search
- Pagination with `limit` and `offset`
- Request validation with Pydantic
- HTTP error handling
- Automatic OpenAPI / Swagger documentation
- PostgreSQL persistence
- Database schema versioning with Alembic
- Automated API tests
- Isolated PostgreSQL database for integration tests

## Project Structure

```text
licitacoes-api/
├── alembic/
│   └── versions/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   └── licitacao.py
│   │
│   ├── routers/
│   │   └── licitacoes.py
│   │
│   ├── schemas/
│   │   └── licitacao.py
│   │
│   └── services/
│       └── licitacao_service.py
│
├── tests/
│   ├── conftest.py
│   └── test_licitacoes.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

## Architecture

The application separates responsibilities into a few simple layers:

```text
HTTP Request
     |
     v
FastAPI Router
     |
     v
Service Layer
     |
     v
SQLAlchemy
     |
     v
PostgreSQL
```

- **Routers** handle HTTP requests and responses.
- **Schemas** define validation and API contracts.
- **Services** contain application and persistence logic.
- **Models** represent database entities.
- **Core** contains configuration and database setup.

The structure intentionally remains simple to avoid unnecessary abstraction for the current project scope.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/licitacoes/` | List procurement records |
| GET | `/licitacoes/{id}` | Retrieve a record by ID |
| POST | `/licitacoes/` | Create a new record |
| PUT | `/licitacoes/{id}` | Update a record |
| DELETE | `/licitacoes/{id}` | Delete a record |

### Filtering and Pagination

The listing endpoint supports query parameters:

```http
GET /licitacoes/?cidade=campinas
```

```http
GET /licitacoes/?modalidade=concorrencia
```

```http
GET /licitacoes/?limit=10&offset=0
```

Filters can also be combined:

```http
GET /licitacoes/?cidade=camp&modalidade=conc&limit=10&offset=0
```

The API uses case-insensitive partial matching for text filters.

Example response:

```json
{
  "items": [
    {
      "titulo": "Reforma e ampliação de escola municipal",
      "cidade": "Paulínia",
      "valor_estimado": "1250000.50",
      "modalidade": "Concorrência",
      "id": 1,
      "criado_em": "2026-09-08T18:00:00Z",
      "atualizado_em": "2026-09-08T18:00:00Z"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

## Running with Docker

Docker is the easiest way to run the application.

### 1. Clone the repository

```bash
git clone https://github.com/pedrohsevaristo/licitacoes-api.git
cd licitacoes-api
```

### 2. Create the environment file

Copy `.env.example` to `.env` and configure the variables:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/licitacoes_db
TEST_DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/licitacoes_test_db

POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=licitacoes_db
```

Do not commit the `.env` file.

### 3. Start the containers

```bash
docker compose up --build
```

Docker Compose starts:

- PostgreSQL
- FastAPI application

The API container automatically applies pending Alembic migrations before starting the application.

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

ReDoc documentation:

```text
http://localhost:8000/redoc
```

To stop the containers:

```bash
docker compose down
```

## Running Locally

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL

Create the application database:

```sql
CREATE DATABASE licitacoes_db;
```

Create a separate test database:

```sql
CREATE DATABASE licitacoes_test_db;
```

Configure both connections in `.env`.

### 4. Apply database migrations

```bash
alembic upgrade head
```

### 5. Start the API

```bash
uvicorn main:app --reload
```

## Database Migrations

Database schema changes are managed with Alembic.

Create a new migration:

```bash
alembic revision --autogenerate -m "migration description"
```

Apply all pending migrations:

```bash
alembic upgrade head
```

The project does not create production tables automatically with `Base.metadata.create_all()`. Schema evolution is versioned through migrations.

## Automated Tests

The project includes integration tests for the main API behavior.

Run:

```bash
python -m pytest -v
```

Current scenarios include:

- Creating a procurement record
- Listing records
- Retrieving by ID
- Handling nonexistent records with `404`
- Updating records
- Deleting records
- Filtering by city
- Rejecting invalid values with `422`

Tests use a separate PostgreSQL database to avoid modifying development data and to keep database behavior consistent with the application environment.

## Example Request

### Create a procurement record

```http
POST /licitacoes/
Content-Type: application/json
```

```json
{
  "titulo": "Reforma e ampliação de escola municipal",
  "cidade": "Paulínia",
  "valor_estimado": 1250000.50,
  "modalidade": "Concorrência"
}
```

Expected status:

```text
201 Created
```

## Validation and HTTP Status Codes

The API uses standard HTTP semantics:

| Status | Meaning |
|---|---|
| `200 OK` | Successful query or update |
| `201 Created` | Resource successfully created |
| `204 No Content` | Resource successfully deleted |
| `404 Not Found` | Requested resource does not exist |
| `422 Unprocessable Entity` | Request validation failed |

## Technical Decisions

### PostgreSQL

PostgreSQL was selected as the relational database because the application has structured entities and benefits from constraints, indexes, transactions and strong data types.

### SQLAlchemy 2.0

SQLAlchemy is used as the ORM and database abstraction layer while keeping queries explicit and close to SQL concepts.

### Decimal for monetary values

Procurement values use Python `Decimal` and PostgreSQL `NUMERIC(14, 2)` rather than floating-point types to avoid precision issues with monetary data.

### Alembic migrations

Database changes are versioned using Alembic instead of creating tables automatically during application startup. This makes schema evolution reproducible and auditable.

### Separate test database

Integration tests use an isolated PostgreSQL database. This avoids modifying development data and reduces differences between the test and application database engines.

### Service layer

Persistence logic is kept outside FastAPI route functions. This keeps HTTP concerns separate from application and database logic without introducing unnecessary architectural layers.

### Pagination

List endpoints use `limit` and `offset`, preventing unrestricted retrieval of all records from the database.

## API Documentation

FastAPI automatically generates OpenAPI documentation.

After starting the project:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Future Improvements

Potential future improvements include:

- Authentication and authorization
- Additional procurement search filters
- More advanced sorting
- CI pipeline for automated tests
- Deployment to a cloud environment

These features were intentionally left outside the current scope to keep the project focused on backend API fundamentals.

## Author

Pedro Evaristo

Backend / Full Stack Developer