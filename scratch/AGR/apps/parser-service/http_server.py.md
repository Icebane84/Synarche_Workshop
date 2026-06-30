from fastapi import FastAPI

from common.service import create_http_app

app = create_http_app("Parser Service")
def health():

    return {
        "status": "healthy"
    }


@app.get("/ready")
def ready():

    return {
        "ready": True
    }