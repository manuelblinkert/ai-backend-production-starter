# ai-backend-production-starter

Production-minded FastAPI starter for AI backends with:

- structured settings via `pydantic-settings`
- request ID middleware and JSON logging
- health and LLM routes
- service boundaries for prompt building and LLM client access
- Docker and `docker compose` support
- pytest coverage for config, health, and LLM endpoint behavior

## Quick start

```bash
uv sync
uv run uvicorn ai_backend_starter.main:app --reload
```

## Environment

Copy `.env.example` to `.env` and adjust values as needed.

## Endpoints

- `GET /health`
- `POST /v1/ai-tasks/analyze`
