from fastapi import APIRouter, Depends

from ai_backend_starter.schemas.errors import ErrorResponse
from ai_backend_starter.schemas.llm import LLMRequest, LLMResponse
from ai_backend_starter.services.llm_client import LLMClient, get_llm_client
from ai_backend_starter.services.prompt_builder import build_messages

router = APIRouter(tags=["llm"])


@router.post(
    "/ai-tasks/analyze",
    response_model=LLMResponse,
    responses={503: {"model": ErrorResponse}},
)
async def complete_text(
    payload: LLMRequest,
    llm_client: LLMClient = Depends(get_llm_client),
) -> LLMResponse:
    messages = build_messages(
        user_prompt=payload.prompt,
        system_prompt=payload.system_prompt,
    )
    completion = await llm_client.complete(messages=messages)
    return LLMResponse(text=completion, model=llm_client.model_name)
