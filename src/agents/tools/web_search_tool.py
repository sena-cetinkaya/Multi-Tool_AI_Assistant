import time

from ddgs import DDGS
from ddgs.exceptions import DDGSException
from langchain_core.tools import tool

from src.core.logger import get_logger

logger = get_logger(__name__)

_MAX_ATTEMPTS = 2
_RETRY_DELAY_SECONDS = 1.5


@tool("web_search")
def web_search(query: str) -> str:
    """
    Güncel olaylar, haberler, fiyatlar veya modelin bilgi kesim tarihinden
    sonraki herhangi bir konu hakkında internette arama yapar.

    Args:
        query: Aranacak arama sorgusu (kısa ve net olmalı).

    Returns:
        Arama sonuçlarının başlık, snippet ve link içeren metin özeti, ya da
        arama başarısız olduysa bunu açıklayan bir metin (agent'ın çalışmayı
        durdurmadan devam edebilmesi için exception FIRLATILMAZ).
    """
    last_error: Exception | None = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            logger.info(f"Web araması yapılıyor (deneme {attempt}): '{query}'")

            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=3)

            if not results:
                return "Arama sonucu bulunamadı."

            formatted = []
            for i, item in enumerate(results[:3], start=1):
                title = item.get("title", "Başlıksız")
                snippet = item.get("body", "")[:200]
                link = item.get("href", "")
                formatted.append(f"{i}. {title}\n   {snippet}\n   Kaynak: {link}")

            header = (
                "(Not: Kaynak olarak SADECE aşağıdaki 'Kaynak:' satırlarındaki "
                "URL'leri kullan, başka bir site uydurma.)\n\n"
            )

            return header + "\n\n".join(formatted)

        except (DDGSException, Exception) as exc:  # noqa: BLE001
            last_error = exc
            logger.warning(f"Web arama denemesi {attempt} başarısız: {exc}")
            if attempt < _MAX_ATTEMPTS:
                time.sleep(_RETRY_DELAY_SECONDS)

    logger.error(f"Web araması {_MAX_ATTEMPTS} denemeden sonra başarısız: {last_error}")
    return (
        "Web araması şu anda geçici bir ağ sorunu nedeniyle yapılamadı "
        f"(hata: {last_error}). Elindeki bilgiyle cevap ver ya da kullanıcıya "
        "bu konuda arama yapılamadığını belirt."
    )