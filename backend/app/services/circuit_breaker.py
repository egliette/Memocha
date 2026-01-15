import logging

from openai import AuthenticationError, BadRequestError, RateLimitError
from pybreaker import CircuitBreaker, CircuitBreakerListener

logger = logging.getLogger(__name__)


class LLMCircuitBreakerListener(CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        if new_state.name == "open":
            logger.warning(
                f"Circuit breaker opened for LLM service (was {old_state.name})"
            )
        elif new_state.name == "half_open":
            logger.info(
                f"Circuit breaker half-open for LLM service (was {old_state.name})"
            )
        elif new_state.name == "closed":
            logger.info(
                f"Circuit breaker closed for LLM service (was {old_state.name})"
            )

    def failure(self, cb, exc):
        logger.debug(f"Circuit breaker recorded failure: {exc}")

    def success(self, cb):
        logger.debug(f"Circuit breaker recorded success")


llm_circuit_breaker = CircuitBreaker(
    fail_max=3,
    reset_timeout=60,
    exclude=[RateLimitError, BadRequestError, AuthenticationError],
    listeners=[LLMCircuitBreakerListener()],
)
