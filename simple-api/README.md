# Simple API

A tiny HTTP API with a health endpoint built with FastAPI.

## Setup (local)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Run (local)

Start the server:

```bash
python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Run with Docker

Build the image (run this inside the `simple-api` folder):

```bash
docker build -t simple-api:local .
```

Run the container:

```bash
docker run --rm -p 8000:8000 simple-api:local
```

## Endpoints

* `GET /` - Welcome message
* `GET /health` - Health check endpoint

## Test

Once running, you can test with curl:

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```

Or visit in your browser:

* [http://localhost:8000](http://localhost:8000)
* [http://localhost:8000/health](http://localhost:8000/health)
* [http://localhost:8000/docs](http://localhost:8000/docs) (Interactive API documentation)

## Run with Docker

Build the image:
```bash
docker build -t simple-api:local .

