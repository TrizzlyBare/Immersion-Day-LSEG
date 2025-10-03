# FastAPI Development Environment

This project provides a FastAPI development environment setup for the LSEG Immersion Day.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Visit the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── core/            # Core configuration
│   ├── api/             # API routes
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   └── services/        # Business logic
├── tests/               # Test files
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Environment Variables

Copy `.env.example` to `.env` and configure your environment variables.

## Testing

Run tests with:

```bash
pytest
```
