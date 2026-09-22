import streamlit as st


def render_sidebar():

    st.sidebar.title("🛡️ SentinelAI")

    st.sidebar.caption("Security Intelligence")

    st.sidebar.divider()

    pagina = st.sidebar.radio(
        "Navegação",
        [
            "Dashboard",
            "Monitoramento",
            "Auditoria",
        ],
    )

    st.sidebar.divider()

    st.sidebar.success("● Sistema online")

    st.sidebar.caption("SentinelAI v1.0.0")

    return pagina