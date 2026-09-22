import streamlit as st

from frontend.components.tables import render_access_table


def render_monitoramento(acessos):

    st.title("Monitoramento")

    st.caption(
        "Acompanhamento dos eventos analisados pelo SentinelAI."
    )

    st.divider()

    if not acessos:

        st.info("Nenhum acesso registrado.")

        return


    st.subheader("Eventos recentes")


    for acesso in acessos[:5]:

        risco = acesso.get(
            "nivel_risco",
            "DESCONHECIDO",
        )

        ip = acesso.get(
            "ip_origem",
            "N/A",
        )

        pais = acesso.get(
            "pais",
            "N/A",
        )


        if risco == "ALTO":

            st.error(
                f"🔴 RISCO ALTO | IP: {ip} | País: {pais}"
            )

        elif risco == "MEDIO":

            st.warning(
                f"🟡 RISCO MÉDIO | IP: {ip} | País: {pais}"
            )

        else:

            st.success(
                f"🟢 RISCO BAIXO | IP: {ip} | País: {pais}"
            )


    st.divider()

    st.subheader("Todos os eventos")

    render_access_table(acessos)