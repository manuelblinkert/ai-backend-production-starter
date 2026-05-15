import logging
from contextvars import ContextVar

from pythonjsonlogger.json import JsonFormatter

from ai_backend_starter.config import get_settings

request_id_context: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


def _has_request_id_filter(handler: logging.Handler) -> bool:
    return any(isinstance(log_filter, RequestIDFilter) for log_filter in handler.filters)


def configure_logging() -> None:
    settings = get_settings()
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level.upper())

    if not root_logger.handlers:
        root_logger.addHandler(logging.StreamHandler())

    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
    )

    for handler in root_logger.handlers:
        handler.setFormatter(formatter)
        if not _has_request_id_filter(handler):
            handler.addFilter(RequestIDFilter())
