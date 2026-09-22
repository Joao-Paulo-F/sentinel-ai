import streamlit as st

from frontend.components.tables import render_access_table


def render_auditoria(acessos):

    st.title("Auditoria")

    st.caption(
        "Histórico dos acessos e decisões de segurança."
    )

    st.divider()

    render_access_table(acessos)

    st.divider()

    st.subheader("Resumo da auditoria")


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


    col1.metric("Total", total)

    col2.metric("Permitidos", permitidos)

    col3.metric("Alertas", alertados)

    col4.metric("Bloqueados", bloqueados)