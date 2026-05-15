from fastapi.testclient import TestClient

from ai_backend_starter.main import app
from ai_backend_starter.services.llm_client import get_llm_client


class StubLLMClient:
    model_name = "test-model"

    async def complete(self, messages: list[dict[str, str]]) -> str:
        return f"stubbed: {messages[-1]['content']}"


client = TestClient(app)


def test_llm_endpoint_returns_stubbed_completion() -> None:
    app.dependency_overrides[get_llm_client] = lambda: StubLLMClient()

    response = client.post(
        "/v1/ai-tasks/analyze",
        json={"prompt": "Say hello", "system_prompt": "Be concise"},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "text": "stubbed: Say hello",
        "model": "test-model",
    }
