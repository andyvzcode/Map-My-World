from fastapi import FastAPI
# from settings.database import engine, Base

description = """This is a simple API that allows you to manage places and recommendations."""

V1_PREFIX = "/v1"

app = FastAPI(
    title="Map My World",
    version="0.0.1",
    description=description,
    openapi_url=f"{V1_PREFIX}/openapi.json",
    docs_url=f"{V1_PREFIX}/docs",)

@app.get("/health/readiness/", tags=["Health"], status_code=200)
def health() -> dict:
    """
    Checks the readiness of the application for Kubernetes.

    ## Returns:
        A dictionary indicating the status of the readiness check. If the application is ready to serve requests,
        returns {"Ok": "I am alive"}. If the application is not yet ready, returns a different status code
        indicating the cause of the unavailability.
    """
    response = {"ok": "I am alive"}
    return response
