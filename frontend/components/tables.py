import pandas as pd
import streamlit as st

from frontend.components.cards import (
    RISK_STYLES,
    ACTION_STYLES,
    action_badge,
    format_datetime,
    html,
    icon,
    risk_badge,
    safe,
    score_bar,
    score_int,
)


RISK_LABELS = {
    "BAIXO": "🟢 Baixo",
    "MEDIO": "🟡 Médio",
    "ALTO": "🔴 Alto",
}

ACTION_LABELS = {
    "PERMITIR": "✅ Permitir",
    "ALERTAR": "⚠️ Alertar",
    "BLOQUEAR": "⛔ Bloquear",
}


def _empty_state(mensagem: str):

    html(
        f"""
        <div class="sx-empty">
            {icon('list', 28, '#475569')}
            <p>{mensagem}</p>
        </div>
        """
    )


# ==========================================================
# TABELA INTERATIVA (ordenável / pesquisável)
# ==========================================================

def render_access_table(acessos):

    if not acessos:

        _empty_state("Nenhum acesso registrado.")

        return


    dados = []


    for acesso in acessos:

        nivel = str(acesso.get("nivel_risco") or "").upper()
        resultado = str(acesso.get("resultado") or "").upper()

        dados.append(
            {
                "ID": acesso.get("id_acesso"),
                "Usuário": acesso.get("id_usuario"),
                "IP": acesso.get("ip_origem"),
                "País": acesso.get("pais"),
                "Cidade": acesso.get("cidade"),
                "Data/Hora": format_datetime(acesso.get("data_hora")),
                "Pontuação": score_int(acesso.get("pontuacao")),
                "Risco": RISK_LABELS.get(nivel, nivel or "—"),
                "Resultado": ACTION_LABELS.get(resultado, resultado or "—"),
                "Motivo": acesso.get("motivo"),
            }
        )


    df = pd.DataFrame(dados)


    cores_risco = {
        RISK_LABELS[chave]: estilo["color"]
        for chave, estilo in RISK_STYLES.items()
    }

    cores_acao = {
        ACTION_LABELS[chave]: estilo["color"]
        for chave, estilo in ACTION_STYLES.items()
    }


    def _cor(valor, mapa):
        cor = mapa.get(valor)
        return f"color: {cor}; font-weight: 600" if cor else ""


    estilizado = df.style

    # pandas >= 2.1 usa .map; versões anteriores usam .applymap
    aplicar = getattr(estilizado, "map", None) or estilizado.applymap
    estilizado = aplicar(lambda v: _cor(v, cores_risco), subset=["Risco"])

    aplicar = getattr(estilizado, "map", None) or estilizado.applymap
    estilizado = aplicar(lambda v: _cor(v, cores_acao), subset=["Resultado"])


    st.dataframe(
        estilizado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn(
                "ID",
                format="#%d",
                width="small",
            ),

            "Usuário": st.column_config.NumberColumn(
                "Usuário",
                format="#%d",
                width="small",
            ),

            "Pontuação": st.column_config.ProgressColumn(
                "Pontuação",
                format="%d/100",
                min_value=0,
                max_value=100,
            ),

            "Risco": st.column_config.TextColumn(
                "Risco"
            ),

            "Resultado": st.column_config.TextColumn(
                "Resultado"
            ),

            "Motivo": st.column_config.TextColumn(
                "Motivos",
                width="large",
            ),
        },
    )


# ==========================================================
# LISTA VISUAL (últimos acessos no dashboard)
# ==========================================================

def render_access_list(acessos):

    if not acessos:

        _empty_state("Nenhum acesso foi registrado ainda.")

        return


    linhas = ""

    for acesso in acessos:

        cidade = safe(acesso.get("cidade"), "")
        pais = safe(acesso.get("pais"))
        local = f"{cidade}, {pais}" if cidade else pais

        linhas += f"""
            <tr>
                <td class="sx-muted">#{safe(acesso.get('id_acesso'), '—')}</td>
                <td>
                    <div class="sx-user">
                        <span class="sx-avatar">{icon('user', 14)}</span>
                        Usuário #{safe(acesso.get('id_usuario'), '—')}
                    </div>
                </td>
                <td><code>{safe(acesso.get('ip_origem'))}</code></td>
                <td>{local}</td>
                <td class="sx-muted">{format_datetime(acesso.get('data_hora'))}</td>
                <td>{score_bar(acesso.get('pontuacao'), '130px')}</td>
                <td>{risk_badge(acesso.get('nivel_risco'))}</td>
                <td>{action_badge(acesso.get('resultado'))}</td>
            </tr>
        """

    html(
        f"""
        <div class="sx-table-wrap">
            <table class="sx-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Usuário</th>
                        <th>IP</th>
                        <th>Localização</th>
                        <th>Data/Hora</th>
                        <th>Pontuação</th>
                        <th>Risco</th>
                        <th>Ação</th>
                    </tr>
                </thead>
                <tbody>{linhas}</tbody>
            </table>
        </div>
        """
    )
