from functools import lru_cache

from fastapi import HTTPException, status
from openai import AsyncOpenAI

from ai_backend_starter.config import get_settings


class LLMClient:
    def __init__(self, api_key: str | None, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self._client = AsyncOpenAI(api_key=api_key) if api_key else None

    async def complete(self, messages: list[dict[str, str]]) -> str:
        if self._client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OPENAI_API_KEY is not configured.",
            )

        response = await self._client.responses.create(
            model=self.model_name,
            input=messages,
        )
        return response.output_text


@lru_cache
def get_llm_client() -> LLMClient:
    settings = get_settings()
    return LLMClient(
        api_key=settings.openai_api_key,
        model_name=settings.openai_model,
    )
