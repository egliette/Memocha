import logging
from typing import Optional

from app.core.config import settings
from app.core.prompts import BASE_SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

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

    def generate_response(self, messages: list) -> str:
        response = self.llm.invoke(messages)
        return response.content

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
