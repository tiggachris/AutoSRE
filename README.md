# AutoSRE - Autonomous Site Reliability Engineering Platform

AutoSRE is an autonomous Site Reliability Engineering (SRE) system designed to monitor, diagnose, remediate, and verify incidents in cloud applications.

## Day 1 Milestone Architecture

- **Web Application**: Flask 3.x REST application serving `/` (homepage) and `/health` (health check with database connectivity probe).
- **Database**: PostgreSQL 16 relational database storing application state and health metrics.
- **Containerization**: Multi-container architecture managed via Docker and Docker Compose.
- **Testing**: Strict Test-Driven Development (TDD) with comprehensive unit and integration test suites using pytest.

## Project Structure

```
AutoSRE/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── config.py            # Environment & database configuration
│   ├── db.py                # Database connection / pool & health checks
│   └── routes.py            # Route blueprints: / and /health
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── unit/
│   │   ├── test_config.py   # Unit tests for configuration
│   │   └── test_db.py       # Unit tests for database logic
│   └── integration/
│       ├── test_routes.py   # Integration tests for HTTP endpoints
│       └── test_db_live.py  # Live container integration tests
├── Dockerfile               # Production container image
├── docker-compose.yml       # Flask & PostgreSQL service orchestration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development and testing dependencies
├── .gitignore
├── .dockerignore
└── README.md
```

## Quickstart

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

### 1. Run with Docker Compose
```bash
docker compose up --build
```
Access the application at `http://localhost:5000`:
- Homepage: `http://localhost:5000/`
- Health check: `http://localhost:5000/health`

### 2. Run Tests Locally
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Or on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Run test suite
pytest -v
```
