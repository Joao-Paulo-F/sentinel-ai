import streamlit as st

from frontend.components.cards import (
    render_page_header,
    render_result_count,
    render_section_title,
    render_stat_card,
)
from frontend.components.tables import render_access_table


def render_auditoria(acessos):

    render_page_header(
        "Auditoria",
        "Histórico e rastreabilidade das decisões de segurança.",
        icone="list",
        etiqueta="Histórico",
    )

    # ======================================================
    # MÉTRICAS
    # ======================================================

    total = len(acessos)

    permitidos = sum(
        1
        for acesso in acessos
        if acesso.get("resultado") == "PERMITIR"
    )

    alertados = sum(
        1
        for acesso in acessos
        if acesso.get("resultado") == "ALERTAR"
    )

    bloqueados = sum(
        1
        for acesso in acessos
        if acesso.get("resultado") == "BLOQUEAR"
    )


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat_card(
            "TOTAL DE EVENTOS", total, "Decisões registradas",
            icone="list", cor="#22D3EE",
        )

    with col2:
        render_stat_card(
            "PERMITIDOS", permitidos, "dos acessos",
            icone="check", cor="#22C55E", total=total,
        )

    with col3:
        render_stat_card(
            "ALERTAS", alertados, "dos acessos",
            icone="bell", cor="#F59E0B", total=total,
        )

    with col4:
        render_stat_card(
            "BLOQUEADOS", bloqueados, "dos acessos",
            icone="lock", cor="#EF4444", total=total,
        )


    # ======================================================
    # FILTRO
    # ======================================================

    render_section_title(
        "Consulta de auditoria",
        "Combine os filtros para localizar registros específicos.",
        icone="search",
    )

    with st.container(border=True):

        col1, col2 = st.columns(2)


        with col1:

            filtro_risco = st.selectbox(
                "Nível de risco",
                [
                    "Todos",
                    "BAIXO",
                    "MEDIO",
                    "ALTO",
                ],
                format_func=lambda v: {
                    "Todos": "Todos os níveis",
                    "BAIXO": "🟢 Baixo",
                    "MEDIO": "🟡 Médio",
                    "ALTO": "🔴 Alto",
                }[v],
            )


        with col2:

            filtro_acao = st.selectbox(
                "Ação de segurança",
                [
                    "Todas",
                    "PERMITIR",
                    "ALERTAR",
                    "BLOQUEAR",
                ],
                format_func=lambda v: {
                    "Todas": "Todas as ações",
                    "PERMITIR": "✅ Permitir",
                    "ALERTAR": "⚠️ Alertar",
                    "BLOQUEAR": "⛔ Bloquear",
                }[v],
            )


    eventos = acessos


    if filtro_risco != "Todos":

        eventos = [
            acesso
            for acesso in eventos
            if acesso.get("nivel_risco") == filtro_risco
        ]


    if filtro_acao != "Todas":

        eventos = [
            acesso
            for acesso in eventos
            if acesso.get("resultado") == filtro_acao
        ]


    render_result_count(
        len(eventos),
        total,
    )


    # ======================================================
    # REGISTROS
    # ======================================================

    render_section_title(
        "Registros",
        "Clique no cabeçalho de uma coluna para ordenar.",
        icone="list",
    )

    render_access_table(eventos)
