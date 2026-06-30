import threading

import uvicorn

from grpc_server import serve

from http_server import app

from config import settings


grpc_thread = threading.Thread(
    target=serve,
    daemon=True,
)

grpc_thread.start()

uvicorn.run(
    app,
    host="0.0.0.0",
    port=settings.http_port,
)