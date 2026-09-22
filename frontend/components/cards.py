import streamlit as st


def render_stat_card(titulo: str, valor: int, descricao: str):

    st.metric(
        label=titulo,
        value=valor,
        help=descricao,
    )