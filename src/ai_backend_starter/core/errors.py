class ConfigurationError(Exception):
    pass


class LLMProviderUnavailableError(Exception):
    def __init__(self, detail: str = "LLM provider unavailable."):
        super().__init__(detail)
        self.detail = detail
