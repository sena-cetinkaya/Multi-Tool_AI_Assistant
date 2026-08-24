import streamlit as st

from config.settings import get_settings
from src.agents.orchestrator import Orchestrator
from src.core.logger import get_logger
from src.core.memory import ConversationMemory
from src.ui.components import render_header, render_sidebar, render_tool_calls
from src.ui.styles import CUSTOM_CSS
from src.utils.exceptions import AgenticChatbotError

logger = get_logger(__name__)

st.set_page_config(
    page_title="Multi-Tool AI Assistant",
    page_icon=":material/workspaces:",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def _init_session_state() -> None:
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = ConversationMemory.new_thread_id()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "orchestrator" not in st.session_state:
        try:
            st.session_state.orchestrator = Orchestrator()
            st.session_state.init_error = None
        except AgenticChatbotError as exc:
            st.session_state.orchestrator = None
            st.session_state.init_error = str(exc)
            logger.error(f"Orchestrator başlatılamadı: {exc}")

def _render_history() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("tool_calls"):
                render_tool_calls(message["tool_calls"])

def main() -> None:
    _init_session_state()
    render_header()
    render_sidebar()

    if st.session_state.init_error:
        st.error(
            "⚠️ Uygulama başlatılamadı:\n\n"
            f"{st.session_state.init_error}"
        )
        st.info(
            "Lütfen proje kökündeki `.env` dosyasına geçerli bir `GROQ_API_KEY` "
            "ekleyip sayfayı yenileyin."
        )
        st.stop()

    _render_history()

    user_input = st.chat_input("Bir şeyler sor...")
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            response = st.session_state.orchestrator.run(
                user_input=user_input,
                thread_id=st.session_state.thread_id,
            )

        st.markdown(response.content)
        render_tool_calls(response.tool_calls)

        if not response.success:
            st.warning(f"Not: {response.error_message}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.content,
            "tool_calls": response.tool_calls,
        }
    )

if __name__ == "__main__":
    settings = get_settings()
    logger.info(f"Agentic Chatbot başlatılıyor (env={settings.app_env})")
    main()
