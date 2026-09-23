import streamlit as st

from frontend.components.tables import render_access_table


def render_auditoria(acessos):

    st.title("Auditoria")

    st.caption(
        "Histórico e rastreabilidade das decisões de segurança."
    )

    st.divider()

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

    col1.metric(
        "Total de eventos",
        total,
    )

    col2.metric(
        "Permitidos",
        permitidos,
    )

    col3.metric(
        "Alertas",
        alertados,
    )

    col4.metric(
        "Bloqueados",
        bloqueados,
    )


    st.divider()


    # ======================================================
    # FILTRO
    # ======================================================

    st.subheader("Consulta de auditoria")

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


    st.caption(
        f"{len(eventos)} evento(s) encontrado(s)"
    )


    st.divider()


    # ======================================================
    # REGISTROS
    # ======================================================

    st.subheader("Registros")

    render_access_table(eventos)