from fastapi import FastAPI

from health import router


def create_http_app(title: str):

    app = FastAPI(
        title=title
    )

    app.include_router(router)

    return app