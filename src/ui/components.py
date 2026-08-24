import streamlit as st

from config.settings import get_settings
from src.models.schemas import ToolCallRecord

_TOOL_ICONS = {
    "web_search": "travel_explore",
    "calculator": "calculate",
    "current_datetime": "schedule",
    "weather": "partly_cloudy_day",
}

def render_header() -> None:
    st.markdown(
        """
        <div class="app-header">
            <span class="material-symbols-outlined">workspaces</span>
            <h1>Multi-Tool AI Assistant</h1>
        </div>
        <div class="app-subtitle">
            Gerektiğinde web'den güncel veri çeken, tool-calling destekli yapay zeka asistanı.
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar() -> None:
    settings = get_settings()

    with st.sidebar:
        st.markdown(
            '<span class="sidebar-section-title">'
            '<span class="material-symbols-outlined">tune</span> Ayarlar</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**Model:** `{settings.llm_model}`")
        st.markdown(f"**Ortam:** `{settings.app_env}`")

        st.markdown("---")
        st.markdown(
            '<span class="sidebar-section-title">'
            '<span class="material-symbols-outlined">construction</span> Aktif Araçlar</span>',
            unsafe_allow_html=True,
        )

        tool_descriptions = [
            ("travel_explore", "web_search", "güncel bilgi araması"),
            ("calculate", "calculator", "güvenli matematik"),
            ("schedule", "current_datetime", "güncel tarih/saat"),
            ("partly_cloudy_day", "weather", "gerçek zamanlı hava durumu"),
        ]
        items_html = "".join(
            f'<div class="tool-list-item">'
            f'<span class="material-symbols-outlined">{icon}</span>'
            f'<code>{name}</code> — {desc}</div>'
            for icon, name, desc in tool_descriptions
        )
        st.markdown(items_html, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Sohbeti Temizle", use_container_width=True):
            st.session_state.clear()
            st.rerun()

def render_tool_calls(tool_calls: list[ToolCallRecord]) -> None:
    if not tool_calls:
        return

    badges = "".join(
        f'<span class="tool-badge">'
        f'<span class="material-symbols-outlined">{_TOOL_ICONS.get(tc.tool_name, "build")}</span>'
        f'{tc.tool_name}</span>'
        for tc in tool_calls
    )
    st.markdown(badges, unsafe_allow_html=True)

    with st.expander("Tool detaylarını göster", expanded=False):
        for tc in tool_calls:
            st.markdown(f"**{tc.tool_name}**")
            st.code(str(tc.tool_input), language="text")
            if tc.tool_output:
                st.text(tc.tool_output[:1500])
            st.divider()