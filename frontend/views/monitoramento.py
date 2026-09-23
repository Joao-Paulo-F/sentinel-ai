import streamlit as st

from frontend.components.tables import render_access_table


def render_monitoramento(acessos):

    st.title("Monitoramento")

    st.caption(
        "Detecção e acompanhamento dos eventos de segurança."
    )

    st.divider()

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

    col1.metric("Eventos", total)
    col2.metric("Risco baixo", baixo)
    col3.metric("Risco médio", medio)
    col4.metric("Risco alto", alto)

    st.divider()

    # ======================================================
    # FILTRO
    # ======================================================

    st.subheader("Filtro de eventos")

    filtro = st.selectbox(
        "Nível de risco",
        [
            "Todos",
            "BAIXO",
            "MEDIO",
            "ALTO",
        ],
    )

    if filtro == "Todos":
        eventos_filtrados = acessos
    else:
        eventos_filtrados = [
            acesso
            for acesso in acessos
            if acesso.get("nivel_risco") == filtro
        ]

    st.caption(
        f"{len(eventos_filtrados)} evento(s) encontrado(s)"
    )

    st.divider()

    # ======================================================
    # EVENTOS
    # ======================================================

    st.subheader("Eventos recentes")

    for acesso in eventos_filtrados[:10]:

        risco = acesso.get(
            "nivel_risco",
            "DESCONHECIDO",
        )

        pontuacao = acesso.get(
            "pontuacao",
            0,
        )

        ip = acesso.get(
            "ip_origem",
            "N/A",
        )

        pais = acesso.get(
            "pais",
            "N/A",
        )

        cidade = acesso.get(
            "cidade",
            "N/A",
        )

        resultado = acesso.get(
            "resultado",
            "N/A",
        )

        data_hora = acesso.get(
            "data_hora",
            "N/A",
        )

        motivo = acesso.get(
            "motivo",
            "Nenhuma anomalia identificada.",
        )

        # -----------------------------------------------
        # RISCO ALTO
        # -----------------------------------------------

        if risco == "ALTO":

            with st.expander(
                f"🔴 RISCO ALTO  •  {pontuacao}/100  •  {resultado}"
            ):

                st.error(
                    "Acesso considerado de alto risco."
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**IP:** {ip}"
                    )

                    st.write(
                        f"**País:** {pais}"
                    )

                    st.write(
                        f"**Cidade:** {cidade}"
                    )

                with col2:

                    st.write(
                        f"**Data/Hora:** {data_hora}"
                    )

                    st.write(
                        f"**Pontuação:** {pontuacao}/100"
                    )

                    st.write(
                        f"**Ação:** {resultado}"
                    )

                st.markdown("**Motivos da detecção:**")

                st.write(motivo)

        # -----------------------------------------------
        # RISCO MÉDIO
        # -----------------------------------------------

        elif risco == "MEDIO":

            with st.expander(
                f"🟡 RISCO MÉDIO  •  {pontuacao}/100  •  {resultado}"
            ):

                st.warning(
                    "Acesso apresenta comportamento fora do padrão."
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**IP:** {ip}"
                    )

                    st.write(
                        f"**País:** {pais}"
                    )

                    st.write(
                        f"**Cidade:** {cidade}"
                    )

                with col2:

                    st.write(
                        f"**Data/Hora:** {data_hora}"
                    )

                    st.write(
                        f"**Pontuação:** {pontuacao}/100"
                    )

                    st.write(
                        f"**Ação:** {resultado}"
                    )

                st.markdown("**Motivos da detecção:**")

                st.write(motivo)

        # -----------------------------------------------
        # RISCO BAIXO
        # -----------------------------------------------

        else:

            with st.expander(
                f"🟢 RISCO BAIXO  •  {pontuacao}/100  •  {resultado}"
            ):

                st.success(
                    "Acesso dentro do comportamento esperado."
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**IP:** {ip}"
                    )

                    st.write(
                        f"**País:** {pais}"
                    )

                    st.write(
                        f"**Cidade:** {cidade}"
                    )

                with col2:

                    st.write(
                        f"**Data/Hora:** {data_hora}"
                    )

                    st.write(
                        f"**Pontuação:** {pontuacao}/100"
                    )

                    st.write(
                        f"**Ação:** {resultado}"
                    )

                st.markdown("**Análise:**")

                st.write(motivo)

    st.divider()

    # ======================================================
    # TABELA
    # ======================================================

    st.subheader("Tabela de eventos")

    render_access_table(eventos_filtrados)