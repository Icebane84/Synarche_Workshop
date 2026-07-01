import structlog


def create_logger(service_name):

    return structlog.get_logger(

        service=service_name

    )
