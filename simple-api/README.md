# Simple API

A tiny HTTP API with a health endpoint built with FastAPI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Run

Start the server:
```bash
python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Test

Once running, visit:
- http://localhost:8000
- http://localhost:8000/health
- http://localhost:8000/docs (Interactive API documentation)
