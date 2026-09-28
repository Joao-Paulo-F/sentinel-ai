from html import escape

import streamlit as st


# ==========================================================
# PALETA / ESTILOS DE RISCO
# ==========================================================

RISK_STYLES = {
    "BAIXO": {
        "label": "Baixo",
        "color": "#22C55E",
        "soft": "rgba(34, 197, 94, 0.12)",
        "icon": "shield-check",
        "mensagem": "Acesso dentro do comportamento esperado.",
    },
    "MEDIO": {
        "label": "Médio",
        "color": "#F59E0B",
        "soft": "rgba(245, 158, 11, 0.12)",
        "icon": "alert",
        "mensagem": "Acesso apresenta comportamento fora do padrão.",
    },
    "ALTO": {
        "label": "Alto",
        "color": "#EF4444",
        "soft": "rgba(239, 68, 68, 0.12)",
        "icon": "shield-x",
        "mensagem": "Acesso considerado de alto risco.",
    },
}

ACTION_STYLES = {
    "PERMITIR": {"label": "Permitido", "color": "#22C55E", "icon": "check"},
    "ALERTAR": {"label": "Alerta", "color": "#F59E0B", "icon": "bell"},
    "BLOQUEAR": {"label": "Bloqueado", "color": "#EF4444", "icon": "lock"},
}

NEUTRAL = {
    "label": "—",
    "color": "#64748B",
    "soft": "rgba(100, 116, 139, 0.12)",
    "icon": "dot",
    "mensagem": "Nível de risco não identificado.",
}


# ==========================================================
# ÍCONES (SVG inline, traço simples)
# ==========================================================

_ICON_PATHS = {
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/>',
    "shield-check": '<path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/>',
    "shield-x": '<path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/><path d="M9.5 9.5l5 5M14.5 9.5l-5 5"/>',
    "alert": '<path d="M12 4l9 16H3l9-16z"/><path d="M12 10v4M12 17h.01"/>',
    "activity": '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    "bell": '<path d="M6 16V11a6 6 0 1112 0v5l2 2H4l2-2z"/><path d="M10 20a2 2 0 004 0"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 118 0v3"/>',
    "check": '<path d="M5 12l5 5 9-10"/>',
    "flame": '<path d="M12 3c1 4 5 5 5 10a5 5 0 01-10 0c0-2 1-3.5 2-4.5 0 2 1 3 2 3 0-3-1-5 1-8.5z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "wifi": '<path d="M4 9a12 12 0 0116 0M7 12.5a7.5 7.5 0 0110 0M10 16a3 3 0 014 0"/><path d="M12 19h.01"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>',
    "server": '<rect x="4" y="4" width="16" height="7" rx="2"/><rect x="4" y="13" width="16" height="7" rx="2"/><path d="M8 7.5h.01M8 16.5h.01"/>',
    "database": '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/><path d="M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    "dot": '<circle cx="12" cy="12" r="4"/>',
}


def icon(nome: str, tamanho: int = 18, cor: str = "currentColor") -> str:

    path = _ICON_PATHS.get(nome, _ICON_PATHS["dot"])

    return (
        f'<svg width="{tamanho}" height="{tamanho}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{cor}" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
    )


# ==========================================================
# UTILITÁRIOS
# ==========================================================

def html(conteudo: str):
    """Renderiza HTML sem que o Markdown do Streamlit
    interprete indentação como bloco de código."""

    compacto = "".join(
        linha.strip()
        for linha in conteudo.splitlines()
    )

    st.markdown(compacto, unsafe_allow_html=True)


def safe(valor, padrao: str = "N/A") -> str:

    if valor is None or valor == "":
        return padrao

    return escape(str(valor))


def risk_style(nivel) -> dict:
    return RISK_STYLES.get(str(nivel or "").upper(), NEUTRAL)


def action_style(acao) -> dict:
    return ACTION_STYLES.get(
        str(acao or "").upper(),
        {"label": safe(acao, "—"), "color": "#64748B", "icon": "dot"},
    )


def score_int(pontuacao) -> int:

    try:
        return int(round(float(pontuacao)))
    except (TypeError, ValueError):
        return 0


def format_datetime(data_hora) -> str:

    if not data_hora:
        return "N/A"

    texto = str(data_hora).replace("T", " ")

    try:
        data, hora = texto.split(" ", 1)
        ano, mes, dia = data.split("-")
        return f"{dia}/{mes}/{ano} {hora[:5]}"
    except ValueError:
        return escape(texto)


def risk_badge(nivel) -> str:

    estilo = risk_style(nivel)

    return (
        f'<span class="sx-badge" style="color:{estilo["color"]};'
        f'background:{estilo["soft"]};border-color:{estilo["color"]}33">'
        f'<span class="sx-dot" style="background:{estilo["color"]}"></span>'
        f'{estilo["label"]}</span>'
    )


def action_badge(acao) -> str:

    estilo = action_style(acao)

    return (
        f'<span class="sx-action" style="color:{estilo["color"]}">'
        f'{icon(estilo["icon"], 14, estilo["color"])}'
        f'{estilo["label"]}</span>'
    )


def score_bar(pontuacao, largura: str = "100%") -> str:

    valor = max(0, min(100, score_int(pontuacao)))

    if valor >= 70:
        cor = RISK_STYLES["ALTO"]["color"]
    elif valor >= 40:
        cor = RISK_STYLES["MEDIO"]["color"]
    else:
        cor = RISK_STYLES["BAIXO"]["color"]

    return (
        f'<div class="sx-score" style="width:{largura}">'
        f'<div class="sx-score-track">'
        f'<div class="sx-score-fill" style="width:{max(valor, 3)}%;background:{cor}"></div>'
        f'</div>'
        f'<span class="sx-score-num">{valor}<small>/100</small></span>'
        f'</div>'
    )


# ==========================================================
# CABEÇALHOS
# ==========================================================

def render_page_header(
    titulo: str,
    subtitulo: str,
    icone: str = "shield",
    etiqueta: str = "",
):

    tag = (
        f'<span class="sx-header-tag">{escape(etiqueta)}</span>'
        if etiqueta
        else ""
    )

    html(
        f"""
        <div class="sx-header">
            <div class="sx-header-icon">{icon(icone, 26, "#22D3EE")}</div>
            <div class="sx-header-text">
                <h1>{escape(titulo)}</h1>
                <p>{escape(subtitulo)}</p>
            </div>
            {tag}
        </div>
        """
    )


def render_section_title(
    titulo: str,
    descricao: str = "",
    icone: str = "",
):

    ico = (
        f'<span class="sx-section-icon">{icon(icone, 16)}</span>'
        if icone
        else ""
    )

    desc = (
        f'<p>{escape(descricao)}</p>'
        if descricao
        else ""
    )

    html(
        f"""
        <div class="sx-section">
            <div class="sx-section-title">{ico}<h3>{escape(titulo)}</h3></div>
            {desc}
        </div>
        """
    )


# ==========================================================
# CARDS DE MÉTRICA
# ==========================================================

def render_stat_card(
    titulo: str,
    valor: int,
    descricao: str,
    icone: str = "activity",
    cor: str = "#22D3EE",
    total: int | None = None,
):

    rodape = escape(descricao)

    progresso = '<div class="sx-stat-progress sx-stat-spacer"></div>'

    if total:
        percentual = round((valor / total) * 100) if total else 0
        progresso = (
            f'<div class="sx-stat-progress">'
            f'<div style="width:{percentual}%;background:{cor}"></div>'
            f'</div>'
        )
        rodape = f'<b style="color:{cor}">{percentual}%</b> · {rodape}'

    html(
        f"""
        <div class="sx-stat" style="--accent:{cor}">
            <div class="sx-stat-top">
                <span class="sx-stat-label">{escape(titulo)}</span>
                <span class="sx-stat-icon" style="color:{cor};background:{cor}1A">
                    {icon(icone, 18, cor)}
                </span>
            </div>
            <div class="sx-stat-value">{valor}</div>
            {progresso}
            <div class="sx-stat-desc">{rodape}</div>
        </div>
        """
    )


# ==========================================================
# DISTRIBUIÇÃO DE RISCO (rosca + barras)
# ==========================================================

def render_risk_distribution(baixo: int, medio: int, alto: int):

    total = baixo + medio + alto

    if total:
        p_baixo = baixo / total * 100
        p_medio = medio / total * 100
        gradiente = (
            f"conic-gradient("
            f"{RISK_STYLES['BAIXO']['color']} 0 {p_baixo:.2f}%,"
            f"#0E1520 {p_baixo:.2f}% calc({p_baixo:.2f}% + 0.6%),"
            f"{RISK_STYLES['MEDIO']['color']} calc({p_baixo:.2f}% + 0.6%) {p_baixo + p_medio:.2f}%,"
            f"#0E1520 {p_baixo + p_medio:.2f}% calc({p_baixo + p_medio:.2f}% + 0.6%),"
            f"{RISK_STYLES['ALTO']['color']} calc({p_baixo + p_medio:.2f}% + 0.6%) 100%)"
        )
    else:
        gradiente = "conic-gradient(#1C2735 0 100%)"

    linhas = ""

    for chave, quantidade in (
        ("BAIXO", baixo),
        ("MEDIO", medio),
        ("ALTO", alto),
    ):
        estilo = RISK_STYLES[chave]
        percentual = round(quantidade / total * 100) if total else 0
        acao = {"BAIXO": "Permitir", "MEDIO": "Alertar", "ALTO": "Bloquear"}[chave]

        linhas += f"""
            <div class="sx-dist-row">
                <div class="sx-dist-head">
                    <span class="sx-dist-name">
                        <span class="sx-dot" style="background:{estilo['color']}"></span>
                        Risco {estilo['label'].lower()}
                        <em>→ {acao}</em>
                    </span>
                    <span class="sx-dist-val"><b>{quantidade}</b> · {percentual}%</span>
                </div>
                <div class="sx-dist-track">
                    <div style="width:{percentual}%;background:{estilo['color']}"></div>
                </div>
            </div>
        """

    html(
        f"""
        <div class="sx-panel sx-dist">
            <div class="sx-donut" style="background:{gradiente}">
                <div class="sx-donut-hole">
                    <span>{total}</span>
                    <small>eventos</small>
                </div>
            </div>
            <div class="sx-dist-rows">{linhas}</div>
        </div>
        """
    )


# ==========================================================
# REGRAS DE PONTUAÇÃO
# ==========================================================

def render_rules_card():

    regras = [
        ("clock", "Fora do horário habitual", 25),
        ("globe", "País diferente do padrão", 35),
        ("cpu", "Dispositivo não reconhecido", 20),
        ("wifi", "IP não reconhecido", 20),
    ]

    itens = "".join(
        f'<div class="sx-rule">'
        f'<span class="sx-rule-icon">{icon(ico, 15)}</span>'
        f'<span class="sx-rule-name">{nome}</span>'
        f'<span class="sx-rule-pts">+{pts}</span>'
        f'</div>'
        for ico, nome, pts in regras
    )

    html(
        f"""
        <div class="sx-panel sx-rules">
            <div class="sx-rules-title">Como a pontuação é calculada</div>
            {itens}
            <div class="sx-scale">
                <span style="--c:#22C55E">0–39 · Baixo</span>
                <span style="--c:#F59E0B">40–69 · Médio</span>
                <span style="--c:#EF4444">70–100 · Alto</span>
            </div>
        </div>
        """
    )


# ==========================================================
# CARD DE EVENTO (monitoramento)
# ==========================================================

def render_event_card(acesso: dict):

    estilo = risk_style(acesso.get("nivel_risco"))

    motivo = acesso.get("motivo") or "Nenhuma anomalia identificada."

    motivos = [
        m.strip()
        for m in str(motivo).split(";")
        if m.strip()
    ]

    sem_anomalia = (
        len(motivos) == 1
        and motivos[0].lower().startswith("nenhuma anomalia")
    )

    if sem_anomalia:
        tags = (
            f'<span class="sx-reason sx-reason-ok">'
            f'{icon("check", 13)} {safe(motivos[0])}</span>'
        )
    else:
        tags = "".join(
            f'<span class="sx-reason" style="color:{estilo["color"]};'
            f'border-color:{estilo["color"]}40;background:{estilo["soft"]}">'
            f'{safe(m)}</span>'
            for m in motivos
        )

    cidade = safe(acesso.get("cidade"), "")
    pais = safe(acesso.get("pais"))
    local = f"{cidade}, {pais}" if cidade else pais

    html(
        f"""
        <div class="sx-event" style="--accent:{estilo['color']}">
            <div class="sx-event-head">
                <div class="sx-event-icon" style="color:{estilo['color']};background:{estilo['soft']}">
                    {icon(estilo['icon'], 20, estilo['color'])}
                </div>
                <div class="sx-event-title">
                    <div class="sx-event-line1">
                        {risk_badge(acesso.get('nivel_risco'))}
                        <span class="sx-event-id">Acesso #{safe(acesso.get('id_acesso'), '—')}</span>
                    </div>
                    <div class="sx-event-msg">{estilo['mensagem']}</div>
                </div>
                <div class="sx-event-side">
                    {action_badge(acesso.get('resultado'))}
                    {score_bar(acesso.get('pontuacao'), '150px')}
                </div>
            </div>
            <div class="sx-event-meta">
                <span>{icon('user', 14)} Usuário #{safe(acesso.get('id_usuario'), '—')}</span>
                <span>{icon('wifi', 14)} <code>{safe(acesso.get('ip_origem'))}</code></span>
                <span>{icon('globe', 14)} {local}</span>
                <span>{icon('clock', 14)} {format_datetime(acesso.get('data_hora'))}</span>
            </div>
            <div class="sx-event-reasons">
                <span class="sx-reasons-label">Motivos da detecção</span>
                {tags}
            </div>
        </div>
        """
    )


# ==========================================================
# STATUS DOS COMPONENTES
# ==========================================================

def render_status_card(titulo: str, descricao: str, icone: str):

    html(
        f"""
        <div class="sx-status">
            <span class="sx-status-icon">{icon(icone, 18, "#22D3EE")}</span>
            <div class="sx-status-text">
                <b>{escape(titulo)}</b>
                <small>{escape(descricao)}</small>
            </div>
            <span class="sx-status-pill"><span class="sx-pulse"></span>Operacional</span>
        </div>
        """
    )


def render_result_count(quantidade: int, total: int):

    html(
        f"""
        <div class="sx-count">
            {icon('search', 14)}
            <span><b>{quantidade}</b> de {total} evento(s) encontrado(s)</span>
        </div>
        """
    )
