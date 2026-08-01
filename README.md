# Sports Store Catalog Service

FastAPI service for product browsing, variants, and internal stock operations. It listens on port `8002`; health is available at `GET /health`.

## Configuration

| Variable | Required | Purpose |
| --- | --- | --- |
| `MONGO_URI` | Yes | MongoDB connection URI for the catalog database. |
| `JWT_SECRET` | Yes | Shared JWT verification secret. |
| `JWT_ALGORITHM` | No | JWT algorithm (default `HS256`). |

`.env.example` contains development-only placeholders. Do not use them in production.

## Build and test

```sh
docker build -t sports-store/catalog-service:0.1.0 .
python -m pytest
```

Run locally with `uvicorn main:app --host 0.0.0.0 --port 8002`.
