import pandas as pd
import streamlit as st


def render_access_table(acessos):

    if not acessos:

        st.info(
            "Nenhum acesso registrado."
        )

        return


    dados = []


    for acesso in acessos:

        dados.append(
            {
                "ID": acesso.get("id_acesso"),
                "Usuário": acesso.get("id_usuario"),
                "IP": acesso.get("ip_origem"),
                "País": acesso.get("pais"),
                "Cidade": acesso.get("cidade"),
                "Data/Hora": acesso.get("data_hora"),
                "Pontuação": acesso.get("pontuacao"),
                "Risco": acesso.get("nivel_risco"),
                "Resultado": acesso.get("resultado"),
            }
        )


    df = pd.DataFrame(dados)


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Pontuação": st.column_config.NumberColumn(
                "Pontuação",
                format="%d/100",
            ),

            "Risco": st.column_config.TextColumn(
                "Risco"
            ),

            "Resultado": st.column_config.TextColumn(
                "Resultado"
            ),
        },
    )