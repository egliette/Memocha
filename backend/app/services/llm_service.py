import logging
from typing import Optional

from app.core.config import settings
from app.core.exceptions import (
    LLMConnectionError,
    LLMRateLimitError,
    LLMServiceError,
    LLMTimeoutError,
)
from app.core.prompts import BASE_SYSTEM_PROMPT
from app.services.circuit_breaker import llm_circuit_breaker
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from openai import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
)
from pybreaker import CircuitBreakerError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


class LLMService:

    def __init__(
        self,
        model_name: str,
        api_key: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        timeout: int = 30,
    ):
        self.llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )

    @llm_circuit_breaker
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type((APIConnectionError, RateLimitError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def generate_response(self, messages: list) -> str:
        try:
            response = self.llm.invoke(messages)
            return response.content
        except CircuitBreakerError as e:
            logger.error(f"Circuit breaker is open: {e}")
            raise LLMServiceError(
                "LLM service is temporily unavailable. Please try again later."
            ) from e
        except RateLimitError as e:
            raise LLMRateLimitError(f"Rate limit exceeded: {str(e)}") from e
        except APITimeoutError as e:
            logger.error(f"Timeout error: {e}")
            raise LLMTimeoutError(f"Request timed out: {str(e)}") from e
        except APIConnectionError as e:
            raise LLMConnectionError(f"Connection failed: {str(e)}") from e
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            raise LLMServiceError(f"Authentication failed: {str(e)}") from e
        except BadRequestError as e:
            logger.error(f"Bad request: {e}")
            raise LLMServiceError(f"Invalid request: {str(e)}") from e
        except APIError as e:
            logger.error(f"API error: {e}")
            raise LLMServiceError(f"LLM API error: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise LLMServiceError(f"Unexpected error: {str(e)}") from e

    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        if system_prompt is None:
            system_prompt = BASE_SYSTEM_PROMPT

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]

        response = self.generate_response(messages)

        if not response or not response.strip():
            logger.warning("Received empty response from LLM")
            return "I apologize, but I couldn't generate a response. Please try again."

        return response


_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService(
            model_name=settings.llm_model,
            api_key=settings.openai_api_key,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
    return _llm_service
