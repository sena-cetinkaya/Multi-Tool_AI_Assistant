from functools import lru_cache

from langchain_groq import ChatGroq

from config.settings import get_settings
from src.core.logger import get_logger
from src.utils.exceptions import ConfigurationError

logger = get_logger(__name__)


@lru_cache
def get_llm() -> ChatGroq:
    settings = get_settings()

    if not settings.groq_api_key:
        raise ConfigurationError(
            "GROQ_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin."
        )

    logger.info(f"LLM istemcisi oluşturuluyor: model={settings.llm_model}")

    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_retries=2,
    )
