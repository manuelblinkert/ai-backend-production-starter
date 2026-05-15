from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    prompt: str = Field(min_length=1)
    system_prompt: str | None = None


class LLMResponse(BaseModel):
    text: str
    model: str
