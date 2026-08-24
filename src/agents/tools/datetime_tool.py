from datetime import datetime, timezone

from langchain_core.tools import tool

from src.core.logger import get_logger

logger = get_logger(__name__)


@tool("current_datetime")
def current_datetime(_: str = "") -> str:
    """
    Şu anki tarih ve saati (UTC) döndürür. Kullanıcı "bugün", "şu an",
    "hangi gündeyiz" gibi zamana bağlı sorular sorduğunda kullanılır.
    """
    now = datetime.now(timezone.utc)
    logger.info("Güncel tarih/saat sorgulandı.")
    return now.strftime("%Y-%m-%d %H:%M:%S UTC, %A")
