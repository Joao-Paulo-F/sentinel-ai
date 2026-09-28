import streamlit as st

from frontend.components.cards import icon


def render_sidebar():

    with st.sidebar:

        st.markdown(
            '<div class="sx-brand">'
            f'<div class="sx-brand-logo">{icon("shield-check", 24, "#070B12")}</div>'
            '<div class="sx-brand-text">'
            '<span class="sx-brand-name">Sentinel<b>AI</b></span>'
            '<span class="sx-brand-sub">Security Intelligence</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sx-nav-label">Navegação</div>',
            unsafe_allow_html=True,
        )

        pagina = st.radio(
            "Navegação",
            [
                "Dashboard",
                "Monitoramento",
                "Auditoria",
            ],
            label_visibility="collapsed",
        )

        st.markdown(
            '<div class="sx-side-footer">'
            '<div class="sx-online">'
            '<span class="sx-pulse"></span>'
            '<div><b>Sistema online</b>'
            '<small>Monitoramento ativo</small></div>'
            '</div>'
            '<div class="sx-version">SentinelAI v1.0.0</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    return pagina
