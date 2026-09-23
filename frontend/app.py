import requests
import streamlit as st

from frontend.components.sidebar import render_sidebar
from frontend.views.dashboard import render_dashboard
from frontend.views.monitoramento import render_monitoramento
from frontend.views.auditoria import render_auditoria


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# VISUAL
# ==========================================================

st.markdown(
    """
    <style>

    /* Fundo principal */
    .stApp {
        background-color: #080C11;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0D131A;
        border-right: 1px solid #1E2A35;
    }

    /* Títulos */
    h1 {
        color: #F2F5F7 !important;
        font-weight: 700 !important;
    }

    h2, h3 {
        color: #DDE5EB !important;
    }

    /* Texto */
    p {
        color: #8C9AA6;
    }

    /* Cards */
    div[data-testid="stMetric"] {
        background-color: #101820;
        border: 1px solid #24313D;
        border-radius: 12px;
        padding: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #82909C !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F5F7F9 !important;
    }

    /* Botões */
    .stButton button {
        border-radius: 8px;
        border: 1px solid #24313D;
        background-color: #101820;
    }

    .stButton button:hover {
        border-color: #00E5FF;
        color: #00E5FF;
    }

    /* Divisores */
    hr {
        border-color: #1E2A35;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# API
# ==========================================================

def buscar_acessos():

    try:

        response = requests.get(
            f"{API_URL}/acessos",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


# ==========================================================
# APLICAÇÃO
# ==========================================================

pagina = render_sidebar()

acessos = buscar_acessos()


if acessos is None:

    st.error("Não foi possível conectar ao SentinelAI.")

    st.info(
        "Verifique se o FastAPI está executando em "
        "http://127.0.0.1:8000"
    )

    st.stop()


if pagina == "Dashboard":

    render_dashboard(acessos)

elif pagina == "Monitoramento":

    render_monitoramento(acessos)

elif pagina == "Auditoria":

    render_auditoria(acessos)