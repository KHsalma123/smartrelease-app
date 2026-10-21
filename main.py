import os

from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="SmartRelease API")

APP_VERSION = os.getenv("APP_VERSION", "v1")
APP_STATUS = os.getenv("APP_STATUS", "healthy")

Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/")
def home():
    return {
        "project": "SmartRelease",
        "version": APP_VERSION,
        "status": APP_STATUS,
        "message": "SmartRelease API v2 - Canary release successful"
    }


@app.get("/health")
def health():
    return {
        "status": APP_STATUS,
        "version": APP_VERSION
    }

@app.get("/test-error")
def test_error():
    raise HTTPException(
        status_code=500,
        detail="SmartRelease controlled failure test"
    )
