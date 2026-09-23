import streamlit as st

from frontend.components.cards import render_stat_card
from frontend.components.tables import render_access_table


def render_dashboard(acessos):

    # ======================================================
    # CABEÇALHO
    # ======================================================

    st.title("🛡️ SentinelAI")

    st.caption(
        "Sistema de Defesa Preditiva e Análise Comportamental"
    )

    st.divider()


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
        )


    with col2:

        render_stat_card(
            "ALERTAS",
            alertas,
            "Acessos que exigiram atenção",
        )


    with col3:

        render_stat_card(
            "BLOQUEIOS",
            bloqueios,
            "Acessos bloqueados",
        )


    with col4:

        render_stat_card(
            "RISCO ALTO",
            risco_alto,
            "Eventos de risco elevado",
        )


    st.markdown("")


    # ======================================================
    # ANÁLISE DE RISCO
    # ======================================================

    st.subheader("Análise de risco")


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
        [2, 1]
    )


    with col_grafico:

        st.bar_chart(
            {
                "Baixo": baixo,
                "Médio": medio,
                "Alto": alto,
            }
        )


    with col_info:

        st.info(
            "O SentinelAI analisa características "
            "do acesso e classifica o nível de risco."
        )

        st.write(
            f"🟢 Baixo: **{baixo}**"
        )

        st.write(
            f"🟡 Médio: **{medio}**"
        )

        st.write(
            f"🔴 Alto: **{alto}**"
        )


    st.divider()


    # ======================================================
    # EVENTOS RECENTES
    # ======================================================

    st.subheader("Últimos acessos")


    if acessos:

        render_access_table(
            acessos[:10]
        )

    else:

        st.info(
            "Nenhum acesso foi registrado ainda."
        )

    st.divider()

    st.subheader("Status do SentinelAI")

    col1, col2, col3 = st.columns(3)

    col1.success("🟢 API operacional")
    col2.success("🟢 Banco de dados operacional")
    col3.success("🟢 Motor de análise operacional")