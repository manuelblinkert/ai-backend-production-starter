import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ai_backend_starter.config import get_settings
from ai_backend_starter.core.errors import LLMProviderUnavailableError
from ai_backend_starter.logging_config import configure_logging
from ai_backend_starter.middleware import RequestIDMiddleware
from ai_backend_starter.routes.health import router as health_router
from ai_backend_starter.routes.llm import router as llm_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    settings = get_settings()
    if not settings.openai_api_key:
        logger.warning(
            "OPENAI_API_KEY is not configured; LLM endpoint will return 503."
        )
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(RequestIDMiddleware)

    @app.exception_handler(LLMProviderUnavailableError)
    async def handle_llm_provider_unavailable(
        request: Request,
        exc: LLMProviderUnavailableError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": exc.detail},
            headers={"x-request-id": getattr(request.state, "request_id", "-")},
        )

    app.include_router(health_router)
    app.include_router(llm_router, prefix="/v1")
    return app


app = create_app()


def main() -> None:
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "ai_backend_starter.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development",
    )
