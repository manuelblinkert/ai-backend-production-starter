import logging
from contextvars import ContextVar

from pythonjsonlogger.json import JsonFormatter

from ai_backend_starter.config import get_settings

request_id_context: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


def configure_logging() -> None:
    settings = get_settings()
    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    handler = logging.StreamHandler()
    handler.addFilter(RequestIDFilter())
    handler.setFormatter(
        JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
        )
    )
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.log_level.upper())
