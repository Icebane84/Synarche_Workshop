from packages.common.config import ServiceConfig

settings = ServiceConfig(
    service_name="validation-service",
    grpc_port=50053,
    http_port=8082,
)