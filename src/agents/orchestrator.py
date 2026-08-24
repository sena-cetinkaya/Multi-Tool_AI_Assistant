from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.messages.utils import count_tokens_approximately, trim_messages
from langgraph.prebuilt import create_react_agent

from config.settings import get_settings
from src.agents.tools import get_tools
from src.core.llm_client import get_llm
from src.core.logger import get_logger
from src.core.memory import ConversationMemory
from src.models.schemas import AgentResponse, ToolCallRecord
from src.utils.exceptions import AgentExecutionError

logger = get_logger(__name__)

SYSTEM_PROMPT = (
    "Sen yardımsever, dürüst ve kısa-öz cevaplar veren bir Türkçe asistansın. "
    "Elindeki tool'ları (web_search, calculator, current_datetime, weather) yalnızca "
    "gerçekten gerekli olduğunda kullan: güncel bilgi veya tarih/saat "
    "gerektirmeyen sorulara doğrudan kendi bilgin ile cevap ver. "
    "Bir tool kullandığında, sonucu kullanıcıya anlaşılır şekilde özetle; "
    "ham tool çıktısını olduğu gibi yapıştırma.\n\n"
    "MATEMATİK KURALI: Ne kadar basit görünürse görünsün (örn. 8*6 gibi), "
    "SAYISAL bir hesaplama içeren HER soru için MUTLAKA 'calculator' "
    "tool'unu çağır. Hesabı asla zihninden/tool'suz yapma; kendi hesabına "
    "güvenme, sonucu her zaman calculator tool'undan doğrula.\n\n"
    "ÖNEMLİ: web_search sonuçları hiçbir zaman %100 kesin/anlık veri "
    "içermeyebilir (örn. tam şu anki sıcaklık gibi). Bir konuda en fazla "
    "2 kez arama yap; ilk aramalar tatmin edici bir kesinlikte sonuç "
    "vermese bile, elindeki en iyi/en güncel bilgiyle kullanıcıya cevap ver "
    "ve gerekirse hangi kaynaktan geldiğini belirt. Aynı veya çok benzer "
    "sorguyu art arda defalarca tekrarlama."
    "\n\nHAVA DURUMU: Hava durumuyla ilgili her soruda (sıcaklık, yağmur, "
    "rüzgar vb.) web_search DEĞİL, 'weather' tool'unu kullan — bu, gerçek "
    "zamanlı ve güvenilir bir meteoroloji API'sinden veri çeker."
    "KAYNAK GÜVENİLİRLİĞİ: Bir web_search sonucundan kaynak (site adı, URL) "
    "belirtirken SADECE tool çıktısında sana verilen 'Kaynak: ...' satırındaki "
    "gerçek URL'i kullan. Tool çıktısında görmediğin bir site adını veya "
    "URL'i asla uydurma/hatırlama. Birden fazla arama sonucu birbiriyle "
    "çelişiyorsa veya kaynaklar tanıdık/güvenilir değilse (resmi kurum, "
    "bilinen haber ajansı, şirketin kendi sitesi değilse), bunu kullanıcıya "
    "açıkça belirt ('bu bilgi doğrulanmamış / tek bir kaynağa dayanıyor' gibi). "
    "Emin olmadığın bir bilgiyi kesinmiş gibi sunmaktansa belirsizliği kabul et."
)


class Orchestrator:
    def __init__(self, memory: ConversationMemory | None = None) -> None:
        settings = get_settings()
        errors = settings.validate_required()
        if errors:
            raise AgentExecutionError(" ".join(errors))

        self._memory = memory or ConversationMemory()
        self._tools = get_tools()
        self._llm = get_llm()

        def _trim_history(state: dict) -> dict:
            trimmed = trim_messages(
                state["messages"],
                strategy="last",
                token_counter=count_tokens_approximately,
                max_tokens=4000,
                start_on="human",
                include_system=True,
            )
            return {"llm_input_messages": trimmed}

        self._graph = create_react_agent(
            model=self._llm,
            tools=self._tools,
            checkpointer=self._memory.checkpointer,
            pre_model_hook=_trim_history,
        )
        logger.info(
            f"Orchestrator hazır. Tool sayısı={len(self._tools)}, "
            f"model={settings.llm_model}"
        )

    def run(self, user_input: str, thread_id: str) -> AgentResponse:
        config = ConversationMemory.build_config(thread_id)
        config["recursion_limit"] = get_settings().max_agent_iterations * 2

        try:
            result = self._graph.invoke(
                {
                    "messages": [
                        SystemMessage(content=SYSTEM_PROMPT),
                        HumanMessage(content=user_input),
                    ]
                },
                config=config,
            )
            return self._parse_result(result)

        except Exception as exc:  # noqa: BLE001
            logger.exception("Agent çalıştırılırken hata oluştu.")
            return AgentResponse(
                content=(
                    "Üzgünüm, isteğini işlerken bir hata oluştu. "
                    "Lütfen tekrar dener misin?"
                ),
                success=False,
                error_message=str(exc),
            )

    @staticmethod
    def _parse_result(result: dict) -> AgentResponse:
        messages = result.get("messages", [])
        tool_calls: list[ToolCallRecord] = []
        final_content = ""

        # Tool çağrısı -> tool sonucu eşleşmesini kur
        pending_calls: dict[str, ToolCallRecord] = {}

        for msg in messages:
            if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
                for call in msg.tool_calls:
                    record = ToolCallRecord(
                        tool_name=call["name"], tool_input=call.get("args", {})
                    )
                    pending_calls[call["id"]] = record
                    tool_calls.append(record)

            elif isinstance(msg, ToolMessage):
                record = pending_calls.get(msg.tool_call_id)
                if record is not None:
                    record.tool_output = str(msg.content)
                    record.success = not str(msg.content).lower().startswith("error")

            elif isinstance(msg, AIMessage) and msg.content:
                final_content = msg.content

        if not final_content and messages:
            last = messages[-1]
            final_content = getattr(last, "content", "") or "Cevap üretilemedi."

        if final_content.strip().lower().startswith("sorry, need more steps"):
            final_content = (
                "Bu istek, elimdeki araçlarla beklediğimden daha fazla adım "
                "gerektirdi ve tamamlanamadan durdu. Sorunu biraz daha "
                "spesifik hale getirip tekrar sorar mısın? (Örn. 'Ankara'da "
                "hava nasıl?' yerine 'Ankara hava durumu bugün' gibi.)"
            )

        return AgentResponse(content=final_content, tool_calls=tool_calls)
