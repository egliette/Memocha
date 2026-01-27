from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    database_url_sync: str
    log_level: str = "INFO"
    openai_api_key: str
    llm_model: str = "gpt-4.1-nano"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = ""


settings = Settings()
