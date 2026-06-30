from pydantic import BaseModel


class Settings(BaseModel):

    service_name: str = "policy-engine"

    grpc_port: int = 50052

    http_port: int = 8081

    policy_directory: str = "/app/policies"

    scm_threshold: float = 0.90


settings = Settings()