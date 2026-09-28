import requests
import streamlit as st

from frontend.components.sidebar import render_sidebar
from frontend.views.dashboard import render_dashboard
from frontend.views.monitoramento import render_monitoramento
from frontend.views.auditoria import render_auditoria


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# VISUAL
# ==========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --sx-bg: #070B12;
    --sx-surface: #0E1520;
    --sx-surface-2: #121B28;
    --sx-border: #1C2735;
    --sx-border-strong: #26344A;
    --sx-text: #E6EDF3;
    --sx-muted: #8B98A9;
    --sx-faint: #5B687A;
    --sx-accent: #22D3EE;
    --sx-accent-2: #6366F1;
    --sx-radius: 14px;
}

/* ---------- Base ---------- */

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.stApp {
    background:
        radial-gradient(1200px 600px at 85% -10%, rgba(34, 211, 238, 0.07), transparent 60%),
        radial-gradient(900px 500px at -10% 10%, rgba(99, 102, 241, 0.07), transparent 60%),
        var(--sx-bg);
    color: var(--sx-text);
}

.block-container {
    padding-top: 2.2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1380px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

code, .sx-score-num, .sx-stat-value, .sx-donut-hole span {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
}

code {
    background: rgba(34, 211, 238, 0.08) !important;
    color: #7DD3FC !important;
    padding: 2px 7px !important;
    border-radius: 6px !important;
    font-size: 0.82em !important;
}

hr {
    border-color: var(--sx-border) !important;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B111A 0%, #080D14 100%);
    border-right: 1px solid var(--sx-border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 0.6rem;
}

.sx-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 4px 22px;
    margin-bottom: 18px;
    border-bottom: 1px solid var(--sx-border);
}

.sx-brand-logo {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #22D3EE 0%, #6366F1 100%);
    box-shadow: 0 8px 24px rgba(34, 211, 238, 0.25);
    flex-shrink: 0;
}

.sx-brand-text {
    display: flex;
    flex-direction: column;
    line-height: 1.15;
}

.sx-brand-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--sx-text);
    letter-spacing: -0.02em;
}

.sx-brand-name b {
    background: linear-gradient(90deg, #22D3EE, #818CF8);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: 800;
}

.sx-brand-sub {
    font-size: 0.66rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--sx-faint);
    margin-top: 3px;
}

.sx-nav-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sx-faint);
    margin: 0 0 8px 4px;
}

/* Rádio da sidebar vira menu de navegação
   (seletores compatíveis com versões antigas e novas do Streamlit) */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 4px !important;
    display: flex;
    flex-direction: column;
    width: 100%;
}

section[data-testid="stSidebar"] div[data-testid="stElementContainer"]:has(div[role="radiogroup"]),
section[data-testid="stSidebar"] div.element-container:has(div[role="radiogroup"]),
section[data-testid="stSidebar"] div[data-testid="stRadio"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div,
section[data-testid="stSidebar"] div[role="radiogroup"] > div {
    width: 100% !important;
    display: flex;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    width: 100%;
    flex: 1;
    box-sizing: border-box;
    margin: 0 !important;
    padding: 11px 14px !important;
    border-radius: 10px;
    border: 1px solid transparent;
    background: transparent;
    transition: all 0.15s ease;
    cursor: pointer;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    font-size: 0.95rem !important;
    font-weight: 500;
    color: var(--sx-muted) !important;
    display: flex;
    align-items: center;
    gap: 12px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p::before {
    content: "";
    width: 18px;
    height: 18px;
    flex-shrink: 0;
    background: currentColor;
    -webkit-mask: var(--sx-nav-icon) center / contain no-repeat;
    mask: var(--sx-nav-icon) center / contain no-repeat;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > :nth-child(1) {
    --sx-nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='3' width='7' height='9' rx='1.5'/%3E%3Crect x='14' y='3' width='7' height='5' rx='1.5'/%3E%3Crect x='14' y='12' width='7' height='9' rx='1.5'/%3E%3Crect x='3' y='16' width='7' height='5' rx='1.5'/%3E%3C/svg%3E");
}

section[data-testid="stSidebar"] div[role="radiogroup"] > :nth-child(2) {
    --sx-nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 12h4l3-8 4 16 3-8h4'/%3E%3C/svg%3E");
}

section[data-testid="stSidebar"] div[role="radiogroup"] > :nth-child(3) {
    --sx-nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01'/%3E%3C/svg%3E");
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.03);
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover p {
    color: var(--sx-text) !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(34, 211, 238, 0.14), rgba(99, 102, 241, 0.06));
    border-color: rgba(34, 211, 238, 0.28);
    box-shadow: inset 3px 0 0 var(--sx-accent);
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: var(--sx-text) !important;
    font-weight: 600;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p::before {
    background: var(--sx-accent);
}

/* Esconde a "bolinha" do rádio (estrutura antiga e nova) */
div[role="radiogroup"] label > div:first-child:not(:has([data-testid="stMarkdownContainer"])),
div[role="radiogroup"] label > div > div:first-child:not([data-testid="stMarkdownContainer"]) {
    display: none !important;
}

.sx-side-footer {
    margin-top: 28px;
    padding-top: 18px;
    border-top: 1px solid var(--sx-border);
}

.sx-online {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    border-radius: 12px;
    background: rgba(34, 197, 94, 0.07);
    border: 1px solid rgba(34, 197, 94, 0.2);
}

.sx-online b {
    display: block;
    font-size: 0.88rem;
    color: #86EFAC;
    font-weight: 600;
}

.sx-online small {
    color: var(--sx-faint);
    font-size: 0.74rem;
}

.sx-version {
    margin: 14px 4px 0;
    font-size: 0.72rem;
    color: var(--sx-faint);
    letter-spacing: 0.04em;
}

/* Indicador pulsante */
.sx-pulse {
    position: relative;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #22C55E;
    flex-shrink: 0;
    display: inline-block;
}

.sx-pulse::after {
    content: "";
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    border: 2px solid #22C55E;
    opacity: 0;
    animation: sx-pulse 2s ease-out infinite;
}

@keyframes sx-pulse {
    0%   { transform: scale(0.5); opacity: 0.8; }
    100% { transform: scale(1.6); opacity: 0; }
}

/* ---------- Cabeçalho de página ---------- */

.sx-header {
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 4px 0 26px;
    margin-bottom: 26px;
    border-bottom: 1px solid var(--sx-border);
}

.sx-header-icon {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, rgba(34, 211, 238, 0.16), rgba(99, 102, 241, 0.16));
    border: 1px solid rgba(34, 211, 238, 0.25);
    flex-shrink: 0;
}

.sx-header-text {
    flex: 1;
    min-width: 0;
}

.sx-header-text h1 {
    margin: 0 !important;
    padding: 0 !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    color: var(--sx-text) !important;
    line-height: 1.15 !important;
}

.sx-header-text p {
    margin: 4px 0 0 !important;
    color: var(--sx-muted) !important;
    font-size: 0.98rem;
}

.sx-header-tag {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--sx-accent);
    padding: 7px 14px;
    border-radius: 999px;
    border: 1px solid rgba(34, 211, 238, 0.3);
    background: rgba(34, 211, 238, 0.07);
    white-space: nowrap;
}

/* ---------- Título de seção ---------- */

.sx-section {
    margin: 34px 0 14px;
}

.sx-section-title {
    display: flex;
    align-items: center;
    gap: 10px;
}

.sx-section-title h3 {
    margin: 0 !important;
    padding: 0 !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: var(--sx-text) !important;
    letter-spacing: -0.01em;
}

.sx-section-icon {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    color: var(--sx-accent);
    background: rgba(34, 211, 238, 0.1);
}

.sx-section p {
    margin: 6px 0 0 38px !important;
    color: var(--sx-faint) !important;
    font-size: 0.86rem;
}

/* ---------- Cards de métrica ---------- */

.sx-stat {
    position: relative;
    overflow: hidden;
    padding: 20px 20px 18px;
    border-radius: var(--sx-radius);
    background: linear-gradient(180deg, var(--sx-surface-2) 0%, var(--sx-surface) 100%);
    border: 1px solid var(--sx-border);
    transition: transform 0.18s ease, border-color 0.18s ease;
    height: 100%;
}

.sx-stat::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent 80%);
}

.sx-stat::after {
    content: "";
    position: absolute;
    top: -60px;
    right: -60px;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: var(--accent);
    opacity: 0.06;
    filter: blur(10px);
}

.sx-stat:hover {
    transform: translateY(-2px);
    border-color: var(--sx-border-strong);
}

.sx-stat-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.sx-stat-label {
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    color: var(--sx-muted);
}

.sx-stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: grid;
    place-items: center;
}

.sx-stat-value {
    font-size: 2.4rem;
    font-weight: 600;
    color: var(--sx-text);
    line-height: 1.1;
    margin: 10px 0 12px;
    letter-spacing: -0.03em;
}

.sx-stat-progress {
    height: 4px;
    border-radius: 99px;
    background: rgba(255, 255, 255, 0.06);
    overflow: hidden;
    margin-bottom: 10px;
}

.sx-stat-progress > div {
    height: 100%;
    border-radius: 99px;
}

.sx-stat-spacer {
    visibility: hidden;
}

.sx-stat-desc {
    font-size: 0.8rem;
    color: var(--sx-faint);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ---------- Painéis ---------- */

.sx-panel {
    border-radius: var(--sx-radius);
    background: var(--sx-surface);
    border: 1px solid var(--sx-border);
    padding: 24px;
    height: 100%;
}

/* Distribuição */
.sx-dist {
    display: flex;
    align-items: center;
    gap: 40px;
    min-height: 304px;
    padding: 28px 32px;
}

.sx-donut {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    box-shadow: 0 0 40px rgba(34, 211, 238, 0.06);
}

.sx-donut-hole {
    width: 142px;
    height: 142px;
    border-radius: 50%;
    background: var(--sx-surface);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.sx-donut-hole span {
    font-size: 2.1rem;
    font-weight: 600;
    color: var(--sx-text);
    line-height: 1;
}

.sx-donut-hole small {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--sx-faint);
    margin-top: 6px;
}

.sx-dist-rows {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-width: 0;
}

.sx-dist-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    gap: 8px;
}

.sx-dist-name {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--sx-text);
}

.sx-dist-name em {
    font-style: normal;
    font-size: 0.78rem;
    color: var(--sx-faint);
    margin-left: 4px;
}

.sx-dist-val {
    font-size: 0.84rem;
    color: var(--sx-muted);
    white-space: nowrap;
}

.sx-dist-val b {
    color: var(--sx-text);
    font-family: 'JetBrains Mono', monospace;
}

.sx-dist-track {
    height: 8px;
    border-radius: 99px;
    background: rgba(255, 255, 255, 0.05);
    overflow: hidden;
}

.sx-dist-track > div {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
}

/* Regras */
.sx-rules-title {
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--sx-muted);
    margin-bottom: 12px;
}

.sx-rule {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 0;
    border-bottom: 1px dashed var(--sx-border);
}

.sx-rule-icon {
    color: var(--sx-accent);
    display: grid;
    place-items: center;
}

.sx-rule-name {
    flex: 1;
    font-size: 0.88rem;
    color: var(--sx-text);
}

.sx-rule-pts {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--sx-accent);
    background: rgba(34, 211, 238, 0.08);
    padding: 2px 8px;
    border-radius: 6px;
}

.sx-scale {
    display: flex;
    gap: 6px;
    margin-top: 16px;
    flex-wrap: wrap;
}

.sx-scale span {
    flex: 1;
    text-align: center;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 6px 4px;
    border-radius: 8px;
    color: var(--c);
    background: color-mix(in srgb, var(--c) 12%, transparent);
    border: 1px solid color-mix(in srgb, var(--c) 30%, transparent);
    white-space: nowrap;
}

/* ---------- Badges ---------- */

.sx-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 600;
    border: 1px solid;
    white-space: nowrap;
}

.sx-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}

.sx-action {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    white-space: nowrap;
}

/* Barra de pontuação */
.sx-score {
    display: flex;
    align-items: center;
    gap: 10px;
}

.sx-score-track {
    flex: 1;
    height: 6px;
    border-radius: 99px;
    background: rgba(255, 255, 255, 0.06);
    overflow: hidden;
}

.sx-score-fill {
    height: 100%;
    border-radius: 99px;
}

.sx-score-num {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--sx-text);
    min-width: 58px;
    text-align: right;
}

.sx-score-num small {
    color: var(--sx-faint);
    font-size: 0.72rem;
}

/* ---------- Tabela visual ---------- */

.sx-table-wrap {
    border-radius: var(--sx-radius);
    border: 1px solid var(--sx-border);
    background: var(--sx-surface);
    overflow-x: auto;
}

.sx-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.87rem;
    margin: 0 !important;
    display: table !important;
}

.sx-table th {
    text-align: left;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--sx-faint) !important;
    padding: 14px 16px !important;
    background: rgba(255, 255, 255, 0.02);
    border: none !important;
    border-bottom: 1px solid var(--sx-border) !important;
    white-space: nowrap;
}

.sx-table td {
    padding: 13px 16px !important;
    color: var(--sx-text);
    border: none !important;
    border-bottom: 1px solid rgba(28, 39, 53, 0.7) !important;
    white-space: nowrap;
    vertical-align: middle;
}

.sx-table tbody tr:last-child td {
    border-bottom: none !important;
}

.sx-table tbody tr {
    transition: background 0.12s ease;
}

.sx-table tbody tr:hover {
    background: rgba(34, 211, 238, 0.035);
}

.sx-muted {
    color: var(--sx-muted) !important;
}

.sx-user {
    display: flex;
    align-items: center;
    gap: 9px;
    font-weight: 500;
}

.sx-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: #A5B4FC;
    background: rgba(99, 102, 241, 0.15);
}

/* ---------- Cards de evento ---------- */

.sx-event {
    position: relative;
    border-radius: var(--sx-radius);
    background: var(--sx-surface);
    border: 1px solid var(--sx-border);
    padding: 18px 20px 16px 24px;
    margin-bottom: 12px;
    overflow: hidden;
    transition: border-color 0.15s ease;
}

.sx-event::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--accent);
}

.sx-event:hover {
    border-color: var(--sx-border-strong);
}

.sx-event-head {
    display: flex;
    align-items: center;
    gap: 14px;
}

.sx-event-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    flex-shrink: 0;
}

.sx-event-title {
    flex: 1;
    min-width: 0;
}

.sx-event-line1 {
    display: flex;
    align-items: center;
    gap: 10px;
}

.sx-event-id {
    font-size: 0.8rem;
    color: var(--sx-faint);
    font-family: 'JetBrains Mono', monospace;
}

.sx-event-msg {
    margin-top: 5px;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--sx-text);
}

.sx-event-side {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
}

.sx-event-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 22px;
    margin: 14px 0 0 56px;
    padding-top: 12px;
    border-top: 1px solid var(--sx-border);
    font-size: 0.84rem;
    color: var(--sx-muted);
}

.sx-event-meta span {
    display: inline-flex;
    align-items: center;
    gap: 7px;
}

.sx-event-meta svg {
    color: var(--sx-faint);
}

.sx-event-reasons {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin: 12px 0 0 56px;
}

.sx-reasons-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--sx-faint);
    margin-right: 4px;
}

.sx-reason {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 8px;
    border: 1px solid;
}

.sx-reason-ok {
    color: #86EFAC;
    background: rgba(34, 197, 94, 0.08);
    border-color: rgba(34, 197, 94, 0.25);
}

/* ---------- Status ---------- */

.sx-status {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 18px;
    border-radius: var(--sx-radius);
    background: var(--sx-surface);
    border: 1px solid var(--sx-border);
}

.sx-status-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: grid;
    place-items: center;
    background: rgba(34, 211, 238, 0.08);
    flex-shrink: 0;
}

.sx-status-text {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.sx-status-text b {
    font-size: 0.92rem;
    color: var(--sx-text);
    font-weight: 600;
}

.sx-status-text small {
    font-size: 0.78rem;
    color: var(--sx-faint);
}

.sx-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.74rem;
    font-weight: 600;
    color: #86EFAC;
    padding: 5px 11px;
    border-radius: 999px;
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.22);
    white-space: nowrap;
}

.sx-status-pill .sx-pulse {
    width: 7px;
    height: 7px;
}

/* ---------- Contador / vazio ---------- */

.sx-count {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 12px;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.82rem;
    color: var(--sx-muted);
    background: var(--sx-surface);
    border: 1px solid var(--sx-border);
}

.sx-count b {
    color: var(--sx-accent);
}

.sx-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 40px 20px;
    border-radius: var(--sx-radius);
    border: 1px dashed var(--sx-border-strong);
    background: var(--sx-surface);
}

.sx-empty p {
    margin: 0 !important;
    color: var(--sx-muted) !important;
}

/* ---------- Widgets nativos ---------- */

/* Filtro horizontal (monitoramento) em formato de pílulas */
.block-container div[role="radiogroup"] {
    gap: 8px !important;
    flex-wrap: wrap;
}

.block-container div[role="radiogroup"] label {
    margin: 0 !important;
    padding: 8px 18px !important;
    border-radius: 999px;
    border: 1px solid var(--sx-border-strong);
    background: var(--sx-surface);
    transition: all 0.15s ease;
    cursor: pointer;
}

.block-container div[role="radiogroup"] label p {
    font-size: 0.88rem !important;
    font-weight: 500;
    color: var(--sx-muted) !important;
}

.block-container div[role="radiogroup"] label:hover {
    border-color: rgba(34, 211, 238, 0.4);
}

.block-container div[role="radiogroup"] label:has(input:checked) {
    background: rgba(34, 211, 238, 0.12);
    border-color: var(--sx-accent);
    box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.08);
}

.block-container div[role="radiogroup"] label:has(input:checked) p {
    color: var(--sx-text) !important;
    font-weight: 600;
}

/* Container com borda (filtros) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--sx-border) !important;
    border-radius: var(--sx-radius) !important;
    background: var(--sx-surface);
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: var(--sx-surface-2) !important;
    border-color: var(--sx-border-strong) !important;
    border-radius: 10px !important;
}

div[data-testid="stSelectbox"] label p {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--sx-muted) !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--sx-border);
    border-radius: var(--sx-radius);
    overflow: hidden;
}

/* Métricas nativas (fallback) */
div[data-testid="stMetric"] {
    background: var(--sx-surface);
    border: 1px solid var(--sx-border);
    border-radius: var(--sx-radius);
    padding: 18px;
}

/* Alertas */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Botões */
.stButton button {
    border-radius: 10px;
    border: 1px solid var(--sx-border-strong);
    background: var(--sx-surface);
    font-weight: 500;
}

.stButton button:hover {
    border-color: var(--sx-accent);
    color: var(--sx-accent);
}

/* Tela de erro de conexão */
.sx-offline {
    max-width: 560px;
    margin: 12vh auto 0;
    text-align: center;
    padding: 44px 36px;
    border-radius: 20px;
    background: var(--sx-surface);
    border: 1px solid var(--sx-border);
}

.sx-offline-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto 18px;
    border-radius: 18px;
    display: grid;
    place-items: center;
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.sx-offline h2 {
    margin: 0 0 8px !important;
    padding: 0 !important;
    font-size: 1.4rem !important;
    color: var(--sx-text) !important;
}

.sx-offline p {
    color: var(--sx-muted) !important;
    margin: 0 0 18px !important;
}

.sx-offline pre {
    text-align: left;
    background: #05080D;
    border: 1px solid var(--sx-border);
    border-radius: 10px;
    padding: 14px 16px;
    color: #7DD3FC;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    margin: 0;
    white-space: pre-wrap;
}

/* ---------- Responsivo ---------- */

@media (max-width: 640px) {
    .sx-stat {
        margin-bottom: 12px;
    }
}

@media (max-width: 900px) {
    .sx-dist {
        flex-direction: column;
        align-items: stretch;
    }

    .sx-donut {
        margin: 0 auto;
    }

    .sx-event-head {
        flex-wrap: wrap;
    }

    .sx-event-side {
        align-items: flex-start;
        width: 100%;
    }

    .sx-event-meta,
    .sx-event-reasons {
        margin-left: 0;
    }

    .sx-header-tag {
        display: none;
    }
}
</style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# API
# ==========================================================

def buscar_acessos():

    try:

        response = requests.get(
            f"{API_URL}/acessos",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


# ==========================================================
# APLICAÇÃO
# ==========================================================

pagina = render_sidebar()

acessos = buscar_acessos()


if acessos is None:

    st.markdown(
        '<div class="sx-offline">'
        '<div class="sx-offline-icon">'
        '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" '
        'stroke="#EF4444" stroke-width="1.8" stroke-linecap="round" '
        'stroke-linejoin="round"><path d="M12 3l7 3v6c0 4.5-3 7.7-7 9-4-1.3-7-4.5-7-9V6l7-3z"/>'
        '<path d="M9.5 9.5l5 5M14.5 9.5l-5 5"/></svg>'
        '</div>'
        '<h2>Não foi possível conectar ao SentinelAI.</h2>'
        f'<p>Verifique se o FastAPI está executando em <code>{API_URL}</code></p>'
        '<pre>python -m uvicorn app.main:app --reload</pre>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.stop()


if pagina == "Dashboard":

    render_dashboard(acessos)

elif pagina == "Monitoramento":

    render_monitoramento(acessos)

elif pagina == "Auditoria":

    render_auditoria(acessos)
