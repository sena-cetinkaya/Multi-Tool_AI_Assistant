from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- LLM Provider (Groq - ücretsiz tier) ---
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    llm_model: str = Field(default="llama-3.3-70b-versatile", alias="LLM_MODEL")
    llm_temperature: float = Field(default=0.3, alias="LLM_TEMPERATURE")

    # --- Application ---
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # --- Agent ---
    max_agent_iterations: int = Field(default=6, alias="MAX_AGENT_ITERATIONS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    def validate_required(self) -> list[str]:
        errors: list[str] = []
        if not self.groq_api_key:
            errors.append(
                "GROQ_API_KEY tanımlı değil. .env dosyasına Groq API anahtarınızı ekleyin "
                "(https://console.groq.com/keys adresinden ücretsiz alabilirsiniz)."
            )
        return errors


@lru_cache
def get_settings() -> Settings:
    return Settings()
