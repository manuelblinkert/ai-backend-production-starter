from functools import lru_cache

from openai import AsyncOpenAI
from openai import OpenAIError

from ai_backend_starter.config import get_settings
from ai_backend_starter.core.errors import LLMProviderUnavailableError


class LLMClient:
    def __init__(self, api_key: str | None, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self._client = AsyncOpenAI(api_key=api_key) if api_key else None

    async def complete(self, messages: list[dict[str, str]]) -> str:
        if self._client is None:
            raise LLMProviderUnavailableError("OPENAI_API_KEY is not configured.")

        try:
            response = await self._client.responses.create(
                model=self.model_name,
                input=messages,
            )
        except OpenAIError as exc:
            raise LLMProviderUnavailableError() from exc

        return response.output_text


@lru_cache
def get_llm_client() -> LLMClient:
    settings = get_settings()
    return LLMClient(
        api_key=settings.openai_api_key,
        model_name=settings.openai_model,
    )
