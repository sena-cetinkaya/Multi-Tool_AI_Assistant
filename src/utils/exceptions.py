class AgenticChatbotError(Exception):
    """Tüm özel hataların türediği taban sınıf."""

class ConfigurationError(AgenticChatbotError):
    """Eksik veya hatalı ortam değişkeni / konfigürasyon durumunda fırlatılır."""

class LLMProviderError(AgenticChatbotError):
    """LLM sağlayıcısına (Groq) yapılan çağrı başarısız olduğunda fırlatılır."""

class ToolExecutionError(AgenticChatbotError):
    """Bir agent tool'u çalıştırılırken hata oluştuğunda fırlatılır."""

class AgentExecutionError(AgenticChatbotError):
    """Orchestrator / agent graph çalıştırılırken beklenmeyen bir hata oluştuğunda fırlatılır."""
