class LLMServiceError(Exception):
    pass


class LLMRateLimitError(Exception):
    pass


class LLMConnectionError(Exception):
    pass


class LLMTimeoutError(Exception):
    pass
