from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    log_level: str = "INFO"
    openai_api_key: str
    llm_model: str = "gpt-4.1-nano"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000

    class Config:
        env_file = ".env"


settings = Settings()
