from packages.common.service import create_http_app


def create_runtime_http(service_name: str):

    return create_http_app(service_name)
