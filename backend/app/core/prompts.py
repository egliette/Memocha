import os

BASE_SYSTEM_PROMPT = os.getenv(
    "BASE_SYSTEM_PROMPT",
    "You are a helpful AI assistant with long-term memory. "
    "You can remember past conversations and use that context to provide "
    "personalized responses. Be concise, helpful, and friendly.",
)
