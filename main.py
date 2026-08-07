import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import products_collection
from observability import configure_observability
from routes import internal, products

logger = logging.getLogger("catalog-service")

app = FastAPI(title="Sports Store — Catalog Service")
configure_observability(app, "catalog-service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api")
app.include_router(internal.router, prefix="/api")


@app.on_event("startup")
async def create_indexes():
    try:
        await products_collection.create_index("slug", unique=True)
        await products_collection.create_index("variants.sku", unique=True)
        await products_collection.create_index("category")
        await products_collection.create_index("tags")
        await products_collection.create_index(
            [("name", "text"), ("description", "text")]
        )
    except Exception:  # Mongo may be unavailable (e.g. unit tests)
        logger.warning(
            "database_index_creation_skipped",
            extra={"event": "database_index_creation_skipped"},
        )


@app.get("/health")
def health():
    return {"status": "ok", "service": "catalog-service"}
