import logging
import structlog


def configure_logging():

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )

    structlog.configure()

    return structlog.get_logger()