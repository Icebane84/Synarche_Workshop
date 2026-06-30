from fastapi import FastAPI

from common.service import create_http_app

app = create_http_app("Policy Engine")


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/ready")
def ready():

    return {
        "ready": True
    }