from fastapi import FastAPI

from db.database import Base, create_db
from routers.categories import categories_router
from routers.locations import locations_router

description = (
    """This is a simple API that allows you to manage places and recommendations."""
)

V1_PREFIX = "/api/v1"

app = FastAPI(
    title="Map My World",
    version="0.0.1",
    description=description,
    openapi_url=f"/openapi.json",
    docs_url=f"/docs",
)


@app.get("/health/readiness/", tags=["Health"], status_code=200)
def health() -> dict:
    """
    ## Returns:
        A dictionary indicating the status of the readiness check. If the application is ready to serve requests,
        returns {"Ok": "I am alive"}. If the application is not yet ready, returns a different status code
        indicating the cause of the unavailability.
    """
    response = {"Ok": "I am alive"}
    return response


@app.on_event("startup")
async def startup():
    db = create_db()
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(
    locations_router, prefix=f"{V1_PREFIX}/locations", tags=["Locations"]
)

app.include_router(
    categories_router, prefix=f"{V1_PREFIX}/categories", tags=["Categories"]
)
