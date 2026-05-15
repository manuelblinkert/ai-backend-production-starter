from ai_backend_starter.config import Settings


def test_settings_read_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "test-app")
    monkeypatch.setenv("APP_PORT", "9000")
    settings = Settings()

    assert settings.app_name == "test-app"
    assert settings.app_port == 9000
