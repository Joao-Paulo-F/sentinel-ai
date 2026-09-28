import streamlit as st

from frontend.components.cards import (
    render_page_header,
    render_risk_distribution,
    render_rules_card,
    render_section_title,
    render_stat_card,
    render_status_card,
)
from frontend.components.tables import render_access_list


def render_dashboard(acessos):

    # ======================================================
    # CABEÇALHO
    # ======================================================

    render_page_header(
        "SentinelAI",
        "Sistema de Defesa Preditiva e Análise Comportamental",
        icone="shield-check",
        etiqueta="Visão geral",
    )


    # ======================================================
    # MÉTRICAS
    # ======================================================

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
            "ACESSOS",
            total,
            "Total de acessos registrados",
            icone="activity",
            cor="#22D3EE",
        )


    with col2:

        render_stat_card(
            "ALERTAS",
            alertas,
            "Acessos que exigiram atenção",
            icone="bell",
            cor="#F59E0B",
            total=total,
        )


    with col3:

        render_stat_card(
            "BLOQUEIOS",
            bloqueios,
            "Acessos bloqueados",
            icone="lock",
            cor="#EF4444",
            total=total,
        )


    with col4:

        render_stat_card(
            "RISCO ALTO",
            risco_alto,
            "Eventos de risco elevado",
            icone="flame",
            cor="#F43F5E",
            total=total,
        )


    # ======================================================
    # ANÁLISE DE RISCO
    # ======================================================

    render_section_title(
        "Análise de risco",
        "Distribuição dos acessos por nível de risco e a ação executada.",
        icone="activity",
    )


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


    col_grafico, col_info = st.columns(
        [3, 2]
    )


    with col_grafico:

        render_risk_distribution(
            baixo,
            medio,
            alto,
        )


    with col_info:

        render_rules_card()


    # ======================================================
    # EVENTOS RECENTES
    # ======================================================

    render_section_title(
        "Últimos acessos",
        "Os 10 eventos mais recentes analisados pelo SentinelAI.",
        icone="list",
    )

    render_access_list(
        acessos[:10]
    )


    # ======================================================
    # STATUS
    # ======================================================

    render_section_title(
        "Status do SentinelAI",
        icone="server",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        render_status_card(
            "API",
            "FastAPI · REST",
            "server",
        )

    with col2:
        render_status_card(
            "Banco de dados",
            "SQLite",
            "database",
        )

    with col3:
        render_status_card(
            "Motor de análise",
            "Regras de risco",
            "cpu",
        )
