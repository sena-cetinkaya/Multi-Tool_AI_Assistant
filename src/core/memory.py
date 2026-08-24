import uuid

from langgraph.checkpoint.memory import MemorySaver

from src.core.logger import get_logger

logger = get_logger(__name__)


class ConversationMemory:
    def __init__(self) -> None:
        self._checkpointer = MemorySaver()

    @property
    def checkpointer(self) -> MemorySaver:
        return self._checkpointer

    @staticmethod
    def new_thread_id() -> str:
        thread_id = str(uuid.uuid4())
        logger.debug(f"Yeni sohbet thread'i oluşturuldu: {thread_id}")
        return thread_id

    @staticmethod
    def build_config(thread_id: str) -> dict:
        return {"configurable": {"thread_id": thread_id}}
