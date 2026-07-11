from packages.common.config import ServiceConfig


class GraphConfig(ServiceConfig):

    postgres_host: str = "postgres"

    postgres_port: int = 5432

    postgres_database: str = "agr"

    postgres_user: str = "agr"

    postgres_password: str = "agr"


settings = GraphConfig(

    service_name="graph-service",

    grpc_port=50054,

    http_port=8083,
)