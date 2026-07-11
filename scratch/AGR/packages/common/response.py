from dataclasses import dataclass


@dataclass
class ServiceResult:

    success: bool

    message: str

    data: dict | None = None