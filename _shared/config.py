# _shared/config.py
# Type-safe configuration via Pydantic Settings.
# One import gives any module validated, env-backed config.
# If a required setting is malformed the app fails at startup, not at query time.
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent.parent / ".env", extra="ignore")

    llm_provider: str = "deepseek"            # openai | gemini | groq | deepseek
    openai_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    deepseek_api_key: str = ""

    embedding_provider: str = "huggingface"  # huggingface | openai
    log_level: str = "INFO"


settings = Settings()
