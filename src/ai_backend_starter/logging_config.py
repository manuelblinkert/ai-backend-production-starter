import logging

from pythonjsonlogger.json import JsonFormatter

from ai_backend_starter.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    handler = logging.StreamHandler()
    handler.setFormatter(
        JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.log_level.upper())
