from pydantic import BaseModel


class ServiceConfig(BaseModel):
    service_name: str
    grpc_port: int
    http_port: int

    log_level: str = "INFO"

    max_workers: int = 16