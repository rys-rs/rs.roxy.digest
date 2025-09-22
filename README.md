# Roxy Digest API

FastAPI service that connects to MongoDB (with JSON fallback) and exposes:

- GET `/menu/{venue_id}/digest`
- GET `/venue/{venue_id}/profile`
- GET `/search?venue_id=&order_type=&reservation=`

## Setup

1. Python 3.10+
2. Create virtual environment and install deps:

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

3. Configure environment (optional if running with JSON fallback):

Copy `.env.example` to `.env` and set your values.

```
MONGO_URI=mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=roxy
```

## Run

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

If MongoDB is not configured or unreachable, the API will transparently use JSON files under `data/` as a fallback.

## Notes

- `order_type` values: `delivery`, `takeout`, `dine-in`.
- Prices in the digest are in cents from the source data.

