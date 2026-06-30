from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = "parser-service"

    grpc_port: int = 50051

    http_port: int = 8080

    max_payload_size: int = 5 * 1024 * 1024


settings = Settings()