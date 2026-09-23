import streamlit as st


def render_sidebar():

    st.sidebar.markdown(
        "# 🛡️ SentinelAI"
    )

    st.sidebar.caption(
        "SECURITY INTELLIGENCE"
    )

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

    st.sidebar.success(
        "● Sistema online"
    )

    st.sidebar.caption(
        "SentinelAI v1.0.0"
    )

    return pagina