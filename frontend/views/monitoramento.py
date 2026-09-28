import streamlit as st

from frontend.components.cards import (
    render_event_card,
    render_page_header,
    render_result_count,
    render_section_title,
    render_stat_card,
)
from frontend.components.tables import render_access_table


FILTROS = {
    "Todos": "Todos",
    "BAIXO": "🟢 Baixo",
    "MEDIO": "🟡 Médio",
    "ALTO": "🔴 Alto",
}


def render_monitoramento(acessos):

    render_page_header(
        "Monitoramento",
        "Detecção e acompanhamento dos eventos de segurança.",
        icone="activity",
        etiqueta="Tempo real",
    )

    if not acessos:
        st.info("Nenhum evento de acesso registrado.")
        return

    # ======================================================
    # RESUMO
    # ======================================================

    total = len(acessos)

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            "EVENTOS", total, "Eventos monitorados",
            icone="activity", cor="#22D3EE",
        )

    with col2:
        render_stat_card(
            "RISCO BAIXO", baixo, "do total",
            icone="shield-check", cor="#22C55E", total=total,
        )

    with col3:
        render_stat_card(
            "RISCO MÉDIO", medio, "do total",
            icone="alert", cor="#F59E0B", total=total,
        )

    with col4:
        render_stat_card(
            "RISCO ALTO", alto, "do total",
            icone="shield-x", cor="#EF4444", total=total,
        )

    # ======================================================
    # FILTRO
    # ======================================================

    render_section_title(
        "Filtro de eventos",
        "Selecione o nível de risco para focar a análise.",
        icone="search",
    )

    filtro = st.radio(
        "Nível de risco",
        list(FILTROS.keys()),
        format_func=lambda chave: FILTROS[chave],
        horizontal=True,
        label_visibility="collapsed",
        key="filtro_monitoramento",
    )

    if filtro == "Todos":
        eventos_filtrados = acessos
    else:
        eventos_filtrados = [
            acesso
            for acesso in acessos
            if acesso.get("nivel_risco") == filtro
        ]

    render_result_count(
        len(eventos_filtrados),
        total,
    )

    # ======================================================
    # EVENTOS
    # ======================================================

    render_section_title(
        "Eventos recentes",
        "Até 10 eventos mais recentes, com os motivos da detecção.",
        icone="bell",
    )

    if not eventos_filtrados:
        st.info("Nenhum evento encontrado para este filtro.")

    for acesso in eventos_filtrados[:10]:

        render_event_card(acesso)

    # ======================================================
    # TABELA
    # ======================================================

    render_section_title(
        "Tabela de eventos",
        "Clique no cabeçalho de uma coluna para ordenar.",
        icone="list",
    )

    render_access_table(eventos_filtrados)
