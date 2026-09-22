import requests
import streamlit as st

from frontend.components.sidebar import render_sidebar
from frontend.pages.dashboard import render_dashboard
from frontend.pages.monitoramento import render_monitoramento
from frontend.pages.auditoria import render_auditoria


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide",
)


st.markdown(
    """
    <style>
        .stApp {
            background-color: #0B0F14;
        }

        section[data-testid="stSidebar"] {
            background-color: #111820;
        }

        h1, h2, h3 {
            color: #F5F5F5;
        }

        p {
            color: #A8B3BE;
        }

        div[data-testid="stMetric"] {
            background-color: #111820;
            border: 1px solid #263340;
            border-radius: 10px;
            padding: 15px;
        }

        div[data-testid="stMetric"] label {
            color: #8A99A8;
        }

        div[data-testid="stMetric"] div {
            color: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def buscar_acessos():

    try:

        response = requests.get(
            f"{API_URL}/acessos",
            timeout=5,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


pagina = render_sidebar()

acessos = buscar_acessos()


if acessos is None:

    st.error("Não foi possível conectar ao SentinelAI.")

    st.info(
        "Verifique se o FastAPI está rodando em "
        "http://127.0.0.1:8000"
    )

    st.stop()


if pagina == "Dashboard":

    render_dashboard(acessos)

elif pagina == "Monitoramento":

    render_monitoramento(acessos)

elif pagina == "Auditoria":

    render_auditoria(acessos)