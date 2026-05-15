from contextlib import asynccontextmanager

from fastapi import FastAPI

from ai_backend_starter.config import get_settings
from ai_backend_starter.logging_config import configure_logging
from ai_backend_starter.middleware import RequestIDMiddleware
from ai_backend_starter.routes.health import router as health_router
from ai_backend_starter.routes.llm import router as llm_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    get_settings()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(RequestIDMiddleware)
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
