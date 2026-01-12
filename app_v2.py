# app.py
# Clean and professional Streamlit dashboard
# Requisitos: streamlit, pandas, requests, matplotlib

import time
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Análise de Deputados Federais",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Clean professional UI (CSS)
# ----------------------------
st.markdown(
    """
<style>
/* Clean light theme */
:root{
  --bg: #F8F9FA;
  --panel: #FFFFFF;
  --text: #212529;
  --muted: #6C757D;
  --border: #DEE2E6;
  --primary: #0D6EFD;
  --primary-light: #E7F1FF;
  --success: #198754;
  --info: #0DCAF0;
}

.block-container { 
  padding-top: 2rem; 
  padding-bottom: 2rem;
  max-width: 1400px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
  background-color: var(--panel);
  border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

/* Typography */
h1 {
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.5rem;
}

h2, h3 {
  font-weight: 600;
  color: var(--text);
}

h3 { 
  font-size: 1.1rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
}

p, label, span { 
  color: var(--text); 
}

.stCaption {
  color: var(--muted) !important;
}

/* Metric cards */
[data-testid="metric-container"]{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

[data-testid="stMetricValue"] {
  font-size: 1.75rem !important;
  font-weight: 700 !important;
  color: var(--primary) !important;
}

[data-testid="stMetricLabel"] {
  color: var(--muted) !important;
  font-size: 0.875rem !important;
  font-weight: 500 !important;
}

/* Buttons */
.stButton > button{
  border-radius: 6px;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border: 1px solid var(--border);
  background: var(--panel);
  color: var(--text);
  transition: all 0.2s ease;
}

.stButton > button:hover{
  background: var(--primary-light);
  border-color: var(--primary);
  color: var(--primary);
}

/* Download button */
.stDownloadButton > button {
  background: var(--primary) !important;
  color: white !important;
  border: none !important;
  font-weight: 500;
}

.stDownloadButton > button:hover {
  background: #0B5ED7 !important;
  box-shadow: 0 2px 4px rgba(13,110,253,0.25);
}

/* Inputs */
[data-baseweb="select"] > div, 
[data-baseweb="input"] input,
.stTextInput input,
.stNumberInput input{
  border-radius: 6px !important;
  border: 1px solid var(--border) !important;
  background-color: var(--panel) !important;
  color: var(--text) !important;
}

[data-baseweb="select"] > div:hover,
[data-baseweb="input"] input:hover,
.stTextInput input:hover{
  border-color: var(--primary) !important;
}

/* Multiselect */
.stMultiSelect [data-baseweb="tag"] {
  background-color: var(--primary-light) !important;
  color: var(--primary) !important;
  border: 1px solid var(--primary) !important;
}

/* Dataframe */
[data-testid="stDataFrame"]{
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

[data-testid="stDataFrame"] thead tr th {
  background: var(--primary-light) !important;
  color: var(--primary) !important;
  font-weight: 600 !important;
  border-bottom: 2px solid var(--primary) !important;
  font-size: 0.875rem !important;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

[data-testid="stDataFrame"] tbody tr:nth-child(odd) {
  background-color: #F8F9FA !important;
}

[data-testid="stDataFrame"] tbody tr:hover {
  background: var(--primary-light) !important;
}

/* Dividers */
hr{ 
  border: none;
  height: 1px;
  background: var(--border);
  margin: 1.5rem 0;
}

/* Tabs */
button[data-baseweb="tab"]{
  font-weight: 500;
  color: var(--muted);
  font-size: 0.95rem;
}

button[data-baseweb="tab"]:hover{
  color: var(--primary);
}

button[data-baseweb="tab"][aria-selected="true"]{
  color: var(--primary);
  border-bottom: 3px solid var(--primary) !important;
  font-weight: 600;
}

/* Links */
a { 
  color: var(--primary);
  text-decoration: none;
}

a:hover {
  color: #0B5ED7;
  text-decoration: underline;
}

/* Expander */
[data-testid="stExpander"] {
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--panel);
}

[data-testid="stExpander"] summary {
  font-weight: 500;
  color: var(--primary);
}

/* Info/Success boxes */
.stInfo {
  background-color: #E7F1FF !important;
  border-left: 4px solid var(--primary) !important;
}

.stSuccess {
  background-color: #D1E7DD !important;
  border-left: 4px solid var(--success) !important;
}

.stError {
  background-color: #F8D7DA !important;
  border-left: 4px solid #DC3545 !important;
}

/* Status badge */
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-success {
  background: #D1E7DD;
  color: #198754;
}

.status-info {
  background: #CFE2FF;
  color: #0D6EFD;
}

.status-warning {
  background: #FFF3CD;
  color: #997404;
}

/* Slider */
.stSlider [data-baseweb="slider"] {
  padding-top: 1.5rem;
}

.stSlider [data-baseweb="slider"] [role="slider"] {
  background-color: var(--primary) !important;
}

.stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
  background-color: var(--primary) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Constants / Helpers
# ----------------------------
BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


def _fmt_int(n: int) -> str:
    return f"{int(n):,}".replace(",", ".")


def _safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default


def _format_timestamp(ts: float) -> str:
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%d/%m/%Y às %H:%M")


# ----------------------------
# Data loading
# ----------------------------
def fetch_deputados_from_api() -> pd.DataFrame:
    url = f"{BASE_URL}/deputados"
    params = {"itens": 1000, "ordem": "ASC", "ordenarPor": "nome"}

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json().get("dados", [])
    df = pd.DataFrame(data)

    expected = ["id", "nome", "siglaPartido", "siglaUf", "uri", "uriPartido", "urlFoto"]
    for c in expected:
        if c not in df.columns:
            df[c] = None

    df["nome"] = df["nome"].astype(str)
    df["siglaPartido"] = df["siglaPartido"].astype(str)
    df["siglaUf"] = df["siglaUf"].astype(str)

    return df


def get_data(ttl_seconds: int, force_refresh: bool) -> tuple[pd.DataFrame, str]:
    now = time.time()

    if "cache_df" not in st.session_state:
        st.session_state.cache_df = pd.DataFrame()
        st.session_state.cache_ts = 0.0
        st.session_state.cache_error = None

    expired = (now - st.session_state.cache_ts) > ttl_seconds
    should_refresh = force_refresh or expired or st.session_state.cache_df.empty

    if not should_refresh:
        return st.session_state.cache_df, "cache"

    try:
        with st.spinner("Carregando dados da API..."):
            df = fetch_deputados_from_api()
        st.session_state.cache_df = df
        st.session_state.cache_ts = now
        st.session_state.cache_error = None
        return df, "api"
    except Exception as e:
        st.session_state.cache_error = str(e)
        if not st.session_state.cache_df.empty:
            return st.session_state.cache_df, "cache_stale"
        return pd.DataFrame(), "error"


def apply_filters(df: pd.DataFrame, partidos_sel, ufs_sel, sort_by: str) -> pd.DataFrame:
    out = df.copy()
    if partidos_sel:
        out = out[out["siglaPartido"].isin(partidos_sel)]
    if ufs_sel:
        out = out[out["siglaUf"].isin(ufs_sel)]
    if sort_by in out.columns:
        out = out.sort_values(sort_by, kind="stable")
    return out.reset_index(drop=True)


def counts_table(series: pd.Series, col_name: str) -> pd.DataFrame:
    vc = series.value_counts()
    return pd.DataFrame({col_name: vc.index, "Quantidade": vc.values})


# ----------------------------
# Charts (matplotlib) - clean style
# ----------------------------
def _style_chart_axes(ax):
    ax.set_facecolor('#FFFFFF')
    ax.tick_params(colors='#6C757D', labelsize=9)
    
    for spine in ax.spines.values():
        spine.set_color('#DEE2E6')
        spine.set_linewidth(1)

    ax.xaxis.label.set_color('#6C757D')
    ax.yaxis.label.set_color('#6C757D')
    ax.title.set_color('#212529')
    ax.title.set_fontsize(12)
    ax.title.set_fontweight('600')

    ax.grid(True, axis='x', color='#DEE2E6', linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)


def chart_partidos_bar(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(20).sort_values()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('#F8F9FA')
    _style_chart_axes(ax)

    bars = ax.barh(counts.index, counts.values, color='#0D6EFD', height=0.65, alpha=0.85)
    
    ax.set_xlabel("Quantidade de Deputados", fontsize=10, fontweight='500')
    ax.set_ylabel("")
    ax.set_title("Top 20 Partidos com Mais Deputados", pad=15)

    maxv = counts.max() if len(counts) else 0
    for i, v in enumerate(counts.values):
        ax.text(v + maxv * 0.01, i, f'{int(v)}', 
                va="center", ha="left", color='#495057', 
                fontsize=8.5, fontweight='500')

    ax.set_xlim(0, maxv * 1.10 if maxv else 1)
    fig.tight_layout()
    return fig


def chart_estados_bar(df: pd.DataFrame):
    counts = df["siglaUf"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('#F8F9FA')
    _style_chart_axes(ax)

    bars = ax.barh(counts.index, counts.values, color='#0DCAF0', height=0.65, alpha=0.85)
    
    ax.set_xlabel("Quantidade de Deputados", fontsize=10, fontweight='500')
    ax.set_ylabel("")
    ax.set_title("Distribuição de Deputados por Estado (UF)", pad=15)

    maxv = counts.max() if len(counts) else 0
    for i, v in enumerate(counts.values):
        ax.text(v + maxv * 0.01, i, f'{int(v)}', 
                va="center", ha="left", color='#495057', 
                fontsize=8.5, fontweight='500')

    ax.set_xlim(0, maxv * 1.10 if maxv else 1)
    fig.tight_layout()
    return fig


def chart_top5_pizza(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(5)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#FFFFFF')

    colors = ['#0D6EFD', '#0DCAF0', '#6610F2', '#FD7E14', '#20C997']

    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'color': '#212529', 'fontsize': 10, 'fontweight': '500'},
        wedgeprops={'linewidth': 2, 'edgecolor': 'white'},
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('700')
        autotext.set_fontsize(10)

    ax.set_title("Top 5 Partidos - Distribuição Percentual", pad=20, fontweight='600', fontsize=12)
    fig.tight_layout()
    return fig


# ----------------------------
# UI components
# ----------------------------
def kpi_row(df: pd.DataFrame):
    total = len(df)
    n_partidos = df["siglaPartido"].nunique(dropna=True)
    n_ufs = df["siglaUf"].nunique(dropna=True)

    top_partido = "-"
    top_qtd = 0
    if total > 0:
        vc = df["siglaPartido"].value_counts()
        if not vc.empty:
            top_partido = vc.index[0]
            top_qtd = _safe_int(vc.iloc[0])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total de Deputados", _fmt_int(total))
    with c2:
        st.metric("Partidos Representados", _fmt_int(n_partidos))
    with c3:
        st.metric("Estados (UFs)", _fmt_int(n_ufs))
    with c4:
        st.metric("Maior Partido", f"{top_partido}", 
                 delta=f"{_fmt_int(top_qtd)} deputados" if top_partido != "-" else None)


def download_csv_button(df: pd.DataFrame, filename: str, label: str = "Exportar CSV"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )


def deputy_details_card(row: dict):
    with st.container():
        col1, col2 = st.columns([1, 2.5])

        with col1:
            foto = row.get("urlFoto")
            if foto and str(foto) != "None":
                st.image(foto, use_container_width=True)
            else:
                st.info("Foto não disponível")

        with col2:
            st.markdown(f"#### {row.get('nome', '-')}")
            st.write(f"**Partido:** {row.get('siglaPartido', '-')}")
            st.write(f"**Estado:** {row.get('siglaUf', '-')}")
            
            uri = row.get("uri")
            if uri and str(uri) != "None":
                st.link_button("Ver dados na API", uri)


def render_table(df: pd.DataFrame, percent_col: str | None = None):
    dfx = df.copy()

    if percent_col and percent_col in dfx.columns:
        total = dfx[percent_col].sum()
        if total > 0:
            dfx["Percentual (%)"] = (dfx[percent_col] / total * 100).round(1)

    st.dataframe(dfx, use_container_width=True, hide_index=True, height=400)


# ----------------------------
# Header
# ----------------------------
st.title("Análise de Deputados Federais")
st.caption("Monitoramento de performance e análise da composição da Câmara dos Deputados")
st.divider()

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("## CONTROLES")

    ttl_minutes = st.number_input(
        "Tempo de cache (minutos)",
        min_value=5,
        max_value=720,
        value=60,
        step=5,
        help="Tempo de validade dos dados em cache",
    )
    ttl_seconds = int(ttl_minutes * 60)

    col_a, col_b = st.columns(2)
    with col_a:
        refresh = st.button("Atualizar", use_container_width=True)
    with col_b:
        clear = st.button("Limpar Cache", use_container_width=True)

    if clear:
        st.session_state.cache_df = pd.DataFrame()
        st.session_state.cache_ts = 0.0
        st.session_state.cache_error = None
        st.success("Cache limpo")

    st.divider()
    st.markdown("## FILTROS")


# ----------------------------
# Load data
# ----------------------------
df, source = get_data(ttl_seconds=ttl_seconds, force_refresh=refresh)

if df.empty:
    err = st.session_state.get("cache_error")
    st.error("Não foi possível carregar os dados.")
    if err:
        with st.expander("Detalhes do erro"):
            st.code(err)
    st.stop()


# ----------------------------
# Filters
# ----------------------------
all_partidos = sorted(df["siglaPartido"].dropna().unique().tolist())
all_ufs = sorted(df["siglaUf"].dropna().unique().tolist())

with st.sidebar:
    partidos_sel = st.multiselect(
        "Partidos", 
        all_partidos, 
        default=[]
    )
    ufs_sel = st.multiselect(
        "Estados (UFs)", 
        all_ufs, 
        default=[]
    )

    active_filters = len(partidos_sel) + len(ufs_sel)
    if active_filters > 0:
        st.info(f"{active_filters} filtro(s) aplicado(s)")

    st.divider()
    st.markdown("## VISUALIZAÇÃO")
    
    sort_by = st.selectbox(
        "Ordenar por", 
        ["nome", "siglaPartido", "siglaUf"], 
        index=0,
        format_func=lambda x: {"nome": "Nome", "siglaPartido": "Partido", "siglaUf": "Estado"}[x]
    )
    page_size = st.selectbox("Linhas por página", [25, 50, 100, 200], index=1)

    st.divider()
    
    # Status display
    if source == "api":
        st.markdown('<span class="status-badge status-success">✓ Dados atualizados</span>', unsafe_allow_html=True)
        if st.session_state.cache_ts:
            st.caption(f"Última atualização: {_format_timestamp(st.session_state.cache_ts)}")
    elif source == "cache":
        st.markdown('<span class="status-badge status-info">Cache ativo</span>', unsafe_allow_html=True)
        if st.session_state.cache_ts:
            st.caption(f"Carregado em: {_format_timestamp(st.session_state.cache_ts)}")
    elif source == "cache_stale":
        st.markdown('<span class="status-badge status-warning">⚠ Cache desatualizado</span>', unsafe_allow_html=True)
        st.caption("API temporariamente indisponível")
    
    st.caption("**Fonte:** Dados Abertos da Câmara")


df_f = apply_filters(df, partidos_sel=partidos_sel, ufs_sel=ufs_sel, sort_by=sort_by)

if active_filters > 0:
    st.info(f"Exibindo {len(df_f):,} de {len(df):,} deputados (filtros aplicados)")


# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(["Visão Geral", "Partidos", "Estados", "Deputados", "Sobre"])


# --- Visão geral ---
with tabs[0]:
    kpi_row(df_f)
    st.divider()

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Distribuição por Partido")
        st.pyplot(chart_partidos_bar(df_f), clear_figure=True)

    with col2:
        st.subheader("Distribuição por Estado")
        st.pyplot(chart_estados_bar(df_f), clear_figure=True)

    with st.expander("Análises Complementares", expanded=False):
        colA, colB = st.columns([1.2, 1.3], gap="medium")
        with colA:
            st.pyplot(chart_top5_pizza(df_f), clear_figure=True)
        with colB:
            st.markdown("### Exportar Dados")
            st.caption("Faça o download dos dados filtrados em formato CSV")
            download_csv_button(df_f, "deputados_filtrados.csv", label="Exportar dados filtrados")

    st.divider()
    download_csv_button(df_f, "deputados_completo.csv", label="Exportar todos os dados")


# --- Partidos ---
with tabs[1]:
    st.subheader("Ranking de Partidos")
    cont_partidos = counts_table(df_f["siglaPartido"], "Partido")
    render_table(cont_partidos, percent_col="Quantidade")

    st.divider()
    download_csv_button(cont_partidos, "ranking_partidos.csv", label="Exportar ranking")


# --- Estados ---
with tabs[2]:
    st.subheader("Ranking por Estado (UF)")
    cont_ufs = counts_table(df_f["siglaUf"], "Estado")
    render_table(cont_ufs, percent_col="Quantidade")

    st.divider()
    download_csv_button(cont_ufs, "ranking_estados.csv", label="Exportar ranking")


# --- Deputados ---
with tabs[3]:
    st.subheader("Buscar Deputados")
    
    col_search, col_total = st.columns([3, 1])
    with col_search:
        search = st.text_input(
            "Digite o nome do deputado", 
            value="", 
            placeholder="Ex: João Silva",
            label_visibility="collapsed"
        )
    with col_total:
        st.metric("Resultados", len(df_f))

    df_view = df_f.copy()
    if search.strip():
        df_view = df_view[df_view["nome"].str.contains(search, case=False, na=False)]
        st.info(f"Encontrados {len(df_view)} resultado(s) para '{search}'")

    # Display table
    table_df = df_view[["nome", "siglaPartido", "siglaUf"]].copy()
    table_df = table_df.rename(columns={
        "nome": "Nome",
        "siglaPartido": "Partido",
        "siglaUf": "Estado"
    })

    st.dataframe(
        table_df.head(page_size), 
        use_container_width=True, 
        hide_index=True,
        height=400
    )

    st.divider()
    st.subheader("Detalhes do Deputado")
    
    options = df_view["nome"].dropna().unique().tolist()
    selected = st.selectbox(
        "Selecione um deputado para ver os detalhes", 
        ["Selecione..."] + options,
        label_visibility="collapsed"
    )

    if selected and selected != "Selecione...":
        row = df_view[df_view["nome"] == selected].iloc[0].to_dict()
        deputy_details_card(row)

    st.divider()
    download_csv_button(df_view, "busca_deputados.csv", label="Exportar resultados da busca")


# --- Sobre ---
with tabs[4]:
    st.markdown("""
### Sobre esta Dashboard

Esta ferramenta foi desenvolvida para facilitar a análise e monitoramento da composição da Câmara dos Deputados do Brasil.

#### Funcionalidades
- **Visualização de dados**: Gráficos interativos mostrando a distribuição de deputados por partido e estado
- **Filtros avançados**: Filtre deputados por partido, estado ou busque por nome
- **Exportação de dados**: Baixe os dados em formato CSV para análises externas
- **Cache inteligente**: Sistema de cache para otimizar o desempenho e reduzir chamadas à API

#### Tecnologias Utilizadas
- **Python** - Linguagem de programação
- **Streamlit** - Framework para criação da interface web
- **Pandas** - Biblioteca para manipulação e análise de dados
- **Matplotlib** - Biblioteca para criação de gráficos

#### Fonte dos Dados
Os dados são obtidos em tempo real através da **API de Dados Abertos da Câmara dos Deputados**, garantindo informações sempre atualizadas sobre a composição do legislativo brasileiro.

#### Configurações Recomendadas
- **Desenvolvimento:** Cache de 5-15 minutos
- **Produção:** Cache de 60-120 minutos
- Use o botão "Atualizar" sempre que precisar dos dados mais recentes

---

*Dashboard desenvolvida para análise transparente de dados públicos.*
    """)
    
    st.info("💡 **Dica:** Mantenha o cache configurado entre 30 e 120 minutos para melhor performance em ambientes de produção.")
