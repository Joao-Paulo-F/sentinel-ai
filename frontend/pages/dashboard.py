import streamlit as st

from frontend.components.cards import render_stat_card
from frontend.components.tables import render_access_table


def render_dashboard(acessos):

    st.title("🛡️ SentinelAI")

    st.caption(
        "Sistema de Defesa Preditiva e Análise Comportamental"
    )

    st.divider()

    total = len(acessos)

    alertas = sum(
        1
        for acesso in acessos
        if acesso.get("resultado") == "ALERTAR"
    )

    bloqueios = sum(
        1
        for acesso in acessos
        if acesso.get("resultado") == "BLOQUEAR"
    )

    risco_alto = sum(
        1
        for acesso in acessos
        if acesso.get("nivel_risco") == "ALTO"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        render_stat_card(
            "Acessos",
            total,
            "Total registrado",
        )


    with col2:
        render_stat_card(
            "Alertas",
            alertas,
            "Requerem atenção",
        )


    with col3:
        render_stat_card(
            "Bloqueios",
            bloqueios,
            "Ações preventivas",
        )


    with col4:
        render_stat_card(
            "Risco alto",
            risco_alto,
            "Eventos críticos",
        )


    st.divider()

    st.subheader("Distribuição de risco")


    baixo = sum(
        1
        for acesso in acessos
        if acesso.get("nivel_risco") == "BAIXO"
    )

    medio = sum(
        1
        for acesso in acessos
        if acesso.get("nivel_risco") == "MEDIO"
    )

    alto = sum(
        1
        for acesso in acessos
        if acesso.get("nivel_risco") == "ALTO"
    )


    grafico = {
        "Baixo": baixo,
        "Médio": medio,
        "Alto": alto,
    }


    st.bar_chart(grafico)


    st.divider()

    st.subheader("Últimos acessos")

    render_access_table(acessos[:10])