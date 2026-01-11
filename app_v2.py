import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
import os
import re
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="SEO Grupo Líder",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# THEME REFINADO
# =========================
st.markdown(
    """
<style>
:root{
  --bg-primary: #fafbfc;
  --bg-secondary: #ffffff;
  --bg-tertiary: #f6f8fa;
  
  --text-primary: #1a1f36;
  --text-secondary: #697386;
  --text-tertiary: #8792a2;
  
  --border-light: #e3e8ee;
  --border-default: #cbd2d9;
  
  --accent-primary: #5469d4;
  --accent-secondary: #0ea5e9;
  --accent-success: #10b981;
  --accent-warning: #f59e0b;
  --accent-danger: #ef4444;
  
  --shadow-sm: 0 1px 3px rgba(50, 50, 93, 0.05), 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(50, 50, 93, 0.08), 0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 15px 35px rgba(50, 50, 93, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07);
  
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
}

.stApp {
  background: linear-gradient(135deg, #f6f8fa 0%, #fafbfc 100%);
  color: var(--text-primary);
}

.block-container {
  padding-top: 2rem;
  max-width: 1400px;
}

/* Header */
.dashboard-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.02em;
}

.dashboard-subtitle {
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-weight: 400;
}

/* Cards e Painéis */
.card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  margin-bottom: 1.5rem;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
}

.card-compact {
  padding: 1rem;
}

/* Section Headers */
.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--border-light);
}

.section-icon {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-primary);
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-left: auto;
}

/* Metric Cards */
.metric-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  opacity: 0;
  transition: opacity 0.2s ease;
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.metric-label {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  line-height: 1;
}

.metric-delta {
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.85rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid var(--border-light);
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
}

.badge-primary {
  background: rgba(84, 105, 212, 0.1);
  border-color: rgba(84, 105, 212, 0.2);
  color: var(--accent-primary);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: 0.5rem;
  background: var(--bg-tertiary);
  padding: 0.25rem;
  border-radius: var(--radius-md);
}

.stTabs [data-baseweb="tab"] {
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  padding: 0.6rem 1.2rem;
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
  background: var(--bg-secondary);
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
  border-radius: var(--radius-md);
  border: 1px solid var(--border-default);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-weight: 500;
  padding: 0.6rem 1.2rem;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.stButton > button:hover, .stDownloadButton > button:hover {
  background: var(--bg-tertiary);
  border-color: var(--accent-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* DataFrames */
div[data-testid="stDataFrame"] {
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

/* Expander */
.streamlit-expanderHeader {
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  font-weight: 500;
}

/* Links */
a {
  color: var(--accent-primary);
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: var(--accent-secondary);
}

/* Responsividade */
@media (max-width: 768px) {
  .dashboard-title {
    font-size: 1.5rem;
  }
  
  .metric-grid {
    grid-template-columns: 1fr;
  }
  
  .section-description {
    display: none;
  }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# UI HELPERS
# =========================
def card_start(compact: bool = False):
    klass = "card card-compact" if compact else "card"
    st.markdown(f"<div class='{klass}'>", unsafe_allow_html=True)

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)

def section_header(title: str, desc: str = ""):
    st.markdown(
        f"""
<div class="section-header">
  <div class="section-icon"></div>
  <h3 class="section-title">{title}</h3>
  {f'<span class="section-description">{desc}</span>' if desc else ''}
</div>
""",
        unsafe_allow_html=True,
    )

def metric_card(label: str, value: str, delta: str):
    st.markdown(
        f"""
<div class="metric-card">
  <div class="metric-label">{label}</div>
  <div class="metric-value">{value}</div>
  <div class="metric-delta">{delta}</div>
</div>
""",
        unsafe_allow_html=True,
    )

def format_int_br(x):
    try:
        return f"{int(round(float(x))):,}".replace(",", ".")
    except Exception:
        return "0"

def futuristic_plotly_light(fig, title=None):
    fig.update_layout(
        template="plotly_white",
        title=title if title else fig.layout.title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(color="#1a1f36", size=13),
        title_font=dict(size=15, color="#1a1f36", family="Arial"),
        colorway=["#5469d4", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444"],
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="rgba(203,210,217,0.5)",
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            bordercolor="#e3e8ee",
        ),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(227,232,238,0.5)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(227,232,238,0.5)", zeroline=False)
    return fig

def download_csv_button(df: pd.DataFrame, filename: str, label: str, key: str):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
        key=key,
    )

# =========================
# DATA EXTRACTION
# =========================
def extract_seo_metrics(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            conteudo = data.get("conteudo", "")

            path_parts = str(Path(json_path)).split(os.sep)
            grupo = path_parts[-3] if len(path_parts) > 2 else ""
            marca = path_parts[-2] if len(path_parts) > 1 else ""

            def extract_number(text):
                numbers = re.findall(r"[\d,.]+", text)
                if numbers:
                    return float(numbers[0].replace(".", "").replace(",", "."))
                return 0

            metrics = {
                "grupo": grupo.replace("grupo-", ""),
                "marca": marca,
                "dominio": "",
                "trafego_organico": 0,
                "trafego_pago": 0,
                "palavras_chave_organicas": 0,
                "palavras_chave_pagas": 0,
                "backlinks": 0,
                "dominos_referencia": 0,
                "posicao_media": 0,
                "ctr": 0,
                "intencao_palavras_chave": {},
                "distribuicao_paises": {},
                "top_palavras": [],
            }

            domain_match = re.search(r"domínio: ([\w\.]+)", conteudo)
            if domain_match:
                metrics["dominio"] = domain_match.group(1)

            for line in conteudo.split("\n"):
                if "Tráfego estimado:" in line and "Resumo da Busca Orgânica" in conteudo.split(line)[0][-50:]:
                    metrics["trafego_organico"] = extract_number(line)
                elif "Palavras-chave orgânicas:" in line:
                    metrics["palavras_chave_organicas"] = extract_number(line)
                elif "Total:" in line and "Backlinks" in conteudo.split(line)[0][-20:]:
                    metrics["backlinks"] = extract_number(line)
                elif "Domínios de referência:" in line:
                    metrics["dominos_referencia"] = extract_number(line)
                elif "Posição no ranking" in line:
                    metrics["posicao_media"] = extract_number(line)

            paises_section = re.search(
                r"Distribuição das Palavras-chave por País \(Busca Orgânica\):(.*?)(?=\n\n)",
                conteudo,
                re.DOTALL,
            )
            if paises_section:
                for line in paises_section.group(1).split("\n"):
                    if ":" in line:
                        pais, percentual = line.split(":")
                        pais = pais.replace("-", "").strip()
                        metrics["distribuicao_paises"][pais] = extract_number(percentual)

            intencao_section = re.search(r"Intenção das Palavras-chave:(.*?)(?=\n\n)", conteudo, re.DOTALL)
            if intencao_section:
                for line in intencao_section.group(1).split("\n"):
                    if ":" in line and "palavras" in line.lower():
                        tipo, resto = line.split(":", 1)
                        tipo = tipo.replace("-", "").strip()
                        palavras = extract_number(resto.split("palavras")[0])
                        trafego = extract_number(resto.split("tráfego")[1]) if "tráfego" in resto else 0
                        percentual = extract_number(resto.split("(")[-1]) if "(" in resto else 0
                        metrics["intencao_palavras_chave"][tipo] = {
                            "palavras": int(palavras),
                            "trafego": int(trafego),
                            "percentual": percentual,
                        }

            palavras_section = re.search(
                r"Principais Palavras-chave Orgânicas:(.*?)(?=\n\nDistribuição das Posições)",
                conteudo,
                re.DOTALL,
            )
            metrics["top_palavras"] = []
            if palavras_section:
                for line in palavras_section.group(1).split("\n"):
                    if '"' in line and "–" in line:
                        partes = line.split("–")
                        if len(partes) >= 3:
                            palavra = partes[0].replace('"', "").strip()
                            volume = extract_number(partes[2])
                            trafego = extract_number(partes[3]) if len(partes) > 3 else 0
                            if palavra and volume > 0:
                                metrics["top_palavras"].append(
                                    {"palavra": palavra, "volume": int(volume), "trafego": trafego}
                                )

            return metrics

    except Exception as e:
        print(f"Erro ao processar {json_path}: {str(e)}")
        return None

@st.cache_data(show_spinner=False)
def load_seo_data(base_dir="analise-performance"):
    all_data = []
    file_count = 0

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json") and "analise_detalhada" in file:
                file_count += 1
                json_path = os.path.join(root, file)
                metrics = extract_seo_metrics(json_path)
                if metrics:
                    all_data.append(metrics)

    return pd.DataFrame(all_data), file_count

# =========================
# HEADER
# =========================
st.markdown(
    """
<div class="dashboard-header">
  <h1 class="dashboard-title">Análise SEO Grupo Líder</h1>
  <p class="dashboard-subtitle">Monitoramento de performance e análise competitiva</p>
</div>
""",
    unsafe_allow_html=True,
)

df_seo, json_files = load_seo_data()

if df_seo is None or df_seo.empty:
    st.warning("Nenhum dado de SEO encontrado. Verifique se os arquivos JSON estão no diretório correto.")
    st.stop()

df_seo["is_lider"] = df_seo["grupo"].astype(str).str.lower().str.contains("lider")
df_seo["marca_display"] = df_seo.apply(
    lambda x: f"{x['marca']} (Grupo Líder)" if x["is_lider"] else x["marca"], axis=1
)

# =========================
# FILTROS
# =========================
card_start(compact=True)
col1, col2, col3, col4 = st.columns([1.5, 2, 1.2, 1])

with col1:
    modo = st.segmented_control(
        "Visão",
        options=["Todos", "Só Grupo Líder", "Só Concorrentes"],
        default="Todos",
    )

with col2:
    marcas = sorted(df_seo["marca_display"].dropna().unique().tolist())
    sel_marcas = st.multiselect("Filtrar por marcas", options=marcas, default=[])

with col3:
    top_n = st.slider("Top concorrentes", 3, 15, 5, 1)

with col4:
    st.markdown(
        f"""
<div style="text-align: right; padding-top: 0.5rem;">
  <span class="badge">{json_files} arquivos</span>
  <span class="badge">{datetime.now().strftime("%d/%m %H:%M")}</span>
</div>
""",
        unsafe_allow_html=True,
    )

card_end()

# Aplicar filtros
df_view = df_seo.copy()

if modo == "Só Grupo Líder":
    df_view = df_view[df_view["is_lider"]]
elif modo == "Só Concorrentes":
    df_view = df_view[~df_view["is_lider"]]

if sel_marcas:
    df_view = df_view[df_view["marca_display"].isin(sel_marcas)]

if df_view.empty:
    st.info("Nenhum dado disponível com os filtros selecionados.")
    st.stop()

# =========================
# FUNÇÕES AUXILIARES
# =========================
def numeric(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)

# =========================
# RESUMO EXECUTIVO
# =========================
card_start()
section_header("Resumo Executivo", "Principais indicadores e oportunidades")

tmp = df_view.copy()
tmp["trafego_organico"] = numeric(tmp["trafego_organico"])
tmp["palavras_chave_organicas"] = numeric(tmp["palavras_chave_organicas"])
tmp["backlinks"] = numeric(tmp["backlinks"])

best_traf = tmp.loc[tmp["trafego_organico"].idxmax()] if not tmp.empty else None
best_kw = tmp.loc[tmp["palavras_chave_organicas"].idxmax()] if not tmp.empty else None
best_back = tmp.loc[tmp["backlinks"].idxmax()] if not tmp.empty else None

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
<span class="badge badge-primary">Maior tráfego: {best_traf['marca_display']}</span><br>
<span class="badge">{format_int_br(best_traf['trafego_organico'])} visitas/mês</span>
""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""
<span class="badge badge-primary">Maior cobertura: {best_kw['marca_display']}</span><br>
<span class="badge">{format_int_br(best_kw['palavras_chave_organicas'])} palavras-chave</span>
""",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""
<span class="badge badge-primary">Maior autoridade: {best_back['marca_display']}</span><br>
<span class="badge">{format_int_br(best_back['backlinks'])} backlinks</span>
""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Análise de oportunidades
q = tmp[["marca_display", "is_lider", "trafego_organico", "backlinks", "palavras_chave_organicas", "dominio"]].copy()
traf_med = q["trafego_organico"].median() if not q.empty else 0
back_med = q["backlinks"].median() if not q.empty else 0

q["quadrante"] = ""
q.loc[(q["backlinks"] >= back_med) & (q["trafego_organico"] < traf_med), "quadrante"] = "Oportunidade"
q.loc[(q["backlinks"] >= back_med) & (q["trafego_organico"] >= traf_med), "quadrante"] = "Líderes"
q.loc[(q["backlinks"] < back_med) & (q["trafego_organico"] >= traf_med), "quadrante"] = "Alto tráfego"
q.loc[(q["backlinks"] < back_med) & (q["trafego_organico"] < traf_med), "quadrante"] = "Em desenvolvimento"

top_op = q[q["quadrante"] == "Oportunidade"].sort_values("backlinks", ascending=False).head(5)

st.markdown("**Oportunidades Identificadas** — Alta autoridade, baixo tráfego")
if top_op.empty:
    st.caption("Nenhuma oportunidade identificada com os filtros atuais.")
else:
    st.dataframe(
        top_op[["marca_display", "dominio", "backlinks", "trafego_organico", "palavras_chave_organicas"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "marca_display": "Marca",
            "dominio": "Domínio",
            "backlinks": st.column_config.NumberColumn("Backlinks", format="%d"),
            "trafego_organico": st.column_config.NumberColumn("Tráfego", format="%d"),
            "palavras_chave_organicas": st.column_config.NumberColumn("Palavras-chave", format="%d"),
        },
    )

card_end()

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["Visão Geral", "Análise Competitiva"])

# =========================
# TAB 1 — VISÃO GERAL
# =========================
with tab1:
    # KPIs do Grupo Líder
    df_lider = df_seo[df_seo["is_lider"]].copy()
    df_lider["trafego_organico"] = numeric(df_lider["trafego_organico"])
    df_lider["palavras_chave_organicas"] = numeric(df_lider["palavras_chave_organicas"])
    df_lider["dominos_referencia"] = numeric(df_lider["dominos_referencia"])

    trafego_lider = float(df_lider["trafego_organico"].sum())
    palavras_lider = float(df_lider["palavras_chave_organicas"].sum())
    dominios_lider = float(df_lider["dominos_referencia"].sum())

    trafego_total_all = float(numeric(df_seo["trafego_organico"]).sum())
    share_lider = (trafego_lider / trafego_total_all * 100) if trafego_total_all > 0 else 0

    card_start()
    section_header("Indicadores do Grupo Líder")
    
    st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)
    metric_card("Tráfego Orgânico", format_int_br(trafego_lider), "visitas mensais")
    metric_card("Palavras-chave", format_int_br(palavras_lider), "termos ranqueados")
    metric_card("Domínios de Referência", format_int_br(dominios_lider), "fontes únicas")
    metric_card("Market Share", f"{share_lider:.1f}%".replace(".", ","), "participação de mercado")
    st.markdown("</div>", unsafe_allow_html=True)
    
    card_end()

    # Palavras-chave principais
    card_start()
    section_header("Principais Palavras-chave", "Termos com maior volume de buscas")

    keywords_data = {"Palavra-chave": [], "Volume": [], "Tráfego": [], "Marca": []}
    for _, row in df_lider.iterrows():
        for kw in row.get("top_palavras", []) or []:
            keywords_data["Palavra-chave"].append(kw.get("palavra", ""))
            keywords_data["Volume"].append(kw.get("volume", 0))
            keywords_data["Tráfego"].append(kw.get("trafego", 0))
            keywords_data["Marca"].append(row.get("marca", ""))

    df_keywords = pd.DataFrame(keywords_data)
    if not df_keywords.empty:
        df_keywords = df_keywords.sort_values("Volume", ascending=False)

        col_a, col_b = st.columns([0.8, 0.2])
        with col_b:
            download_csv_button(df_keywords, "palavras_chave.csv", "Exportar CSV", key="dl_kw")

        st.dataframe(
            df_keywords,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "Volume": st.column_config.NumberColumn("Volume", format="%d"),
                "Tráfego": st.column_config.NumberColumn("Tráfego", format="%.1f"),
            },
        )
    else:
        st.info("Dados de palavras-chave não disponíveis.")

    card_end()

    # Top Concorrentes
    df_concorrentes = df_view[~df_view["is_lider"]].copy()
    df_concorrentes["trafego_organico"] = numeric(df_concorrentes["trafego_organico"])
    df_concorrentes["palavras_chave_organicas"] = numeric(df_concorrentes["palavras_chave_organicas"])
    df_concorrentes["backlinks"] = numeric(df_concorrentes["backlinks"])
    df_concorrentes["dominos_referencia"] = numeric(df_concorrentes["dominos_referencia"])

    card_start()
    section_header(f"Top {top_n} Concorrentes", "Ranking por tráfego orgânico")

    if not df_concorrentes.empty:
        df_top = df_concorrentes.nlargest(top_n, "trafego_organico").copy()

        tbl = pd.DataFrame({
            "Marca": df_top["marca_display"],
            "Domínio": df_top["dominio"],
            "Tráfego": df_top["trafego_organico"].round(0).astype(int),
            "Palavras-chave": df_top["palavras_chave_organicas"].round(0).astype(int),
            "Backlinks": df_top["backlinks"].round(0).astype(int),
            "Domínios Ref.": df_top["dominos_referencia"].round(0).astype(int),
        })

        col_a, col_b = st.columns([0.8, 0.2])
        with col_b:
            download_csv_button(tbl, "top_concorrentes.csv", "Exportar CSV", key="dl_top")

        st.dataframe(
            tbl,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Tráfego": st.column_config.NumberColumn("Tráfego", format="%d"),
                "Palavras-chave": st.column_config.NumberColumn("Palavras-chave", format="%d"),
                "Backlinks": st.column_config.NumberColumn("Backlinks", format="%d"),
                "Domínios Ref.": st.column_config.NumberColumn("Domínios Ref.", format="%d"),
            },
        )

        st.markdown("<br>", unsafe_allow_html=True)

        fig_traf = px.bar(
            df_top,
            x="marca_display",
            y="trafego_organico",
            title="Tráfego Orgânico por Concorrente",
            labels={"marca_display": "Marca", "trafego_organico": "Visitas/mês"},
        )
        fig_traf = futuristic_plotly_light(fig_traf)
        st.plotly_chart(fig_traf, use_container_width=True)
    else:
        st.info("Nenhum concorrente disponível com os filtros atuais.")

    card_end()

    # Comparativo por marca
    card_start()
    section_header("Comparativo por Marca", "Tráfego e cobertura de palavras-chave")

    grouped = (
        df_view.assign(
            trafego_organico=numeric(df_view["trafego_organico"]),
            palavras_chave_organicas=numeric(df_view["palavras_chave_organicas"]),
        )
        .groupby("marca_display")[["trafego_organico", "palavras_chave_organicas"]]
        .sum()
        .reset_index()
    )

    fig_mix = px.bar(
        grouped,
        x="marca_display",
        y=["trafego_organico", "palavras_chave_organicas"],
        barmode="group",
        title="Tráfego e Palavras-chave por Marca",
        labels={"value": "Volume", "variable": "Métrica", "marca_display": "Marca"},
    )
    fig_mix = futuristic_plotly_light(fig_mix)
    st.plotly_chart(fig_mix, use_container_width=True)

    card_end()

# =========================
# TAB 2 — ANÁLISE COMPETITIVA
# =========================
with tab2:
    card_start()
    section_header("Mapa Competitivo", "Autoridade vs Ranking (tamanho = tráfego)")

    df_plot = df_view.copy()
    df_plot["backlinks"] = numeric(df_plot["backlinks"])
    df_plot["posicao_media"] = numeric(df_plot["posicao_media"])
    df_plot["trafego_organico"] = numeric(df_plot["trafego_organico"])
    df_plot["palavras_chave_organicas"] = numeric(df_plot["palavras_chave_organicas"])

    fig_scatter = px.scatter(
        df_plot,
        x="backlinks",
        y="posicao_media",
        size="trafego_organico",
        color="is_lider",
        hover_data=["marca_display", "dominio", "trafego_organico", "palavras_chave_organicas"],
        title="Backlinks vs Posição Média",
        labels={
            "backlinks": "Backlinks (escala log)",
            "posicao_media": "Posição Média (menor = melhor)",
            "is_lider": "Grupo",
        },
        color_discrete_map={True: "#5469d4", False: "#f59e0b"},
    )

    fig_scatter.update_xaxes(type="log")
    
    if len(fig_scatter.data) >= 1:
        for tr in fig_scatter.data:
            if str(tr.name) in ("True", "true"):
                tr.name = "Grupo Líder"
            elif str(tr.name) in ("False", "false"):
                tr.name = "Concorrentes"

    fig_scatter = futuristic_plotly_light(fig_scatter)
    fig_scatter.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "Domínio: %{customdata[1]}<br>"
        "Tráfego: %{customdata[2]:,.0f}<br>"
        "Keywords: %{customdata[3]:,.0f}<br>"
        "Backlinks: %{x:,.0f}<br>"
        "Posição média: %{y:,.1f}<br>"
        "<extra></extra>"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)
    card_end()

    # Tabela completa
    card_start()
    section_header("Métricas Consolidadas", "Todos os indicadores por marca")

    metricas = (
        df_view.assign(
            trafego_organico=numeric(df_view["trafego_organico"]),
            palavras_chave_organicas=numeric(df_view["palavras_chave_organicas"]),
            backlinks=numeric(df_view["backlinks"]),
            dominos_referencia=numeric(df_view["dominos_referencia"]),
            posicao_media=numeric(df_view["posicao_media"]),
        )
        .groupby("marca_display")
        .agg({
            "trafego_organico": "sum",
            "palavras_chave_organicas": "sum",
            "backlinks": "sum",
            "dominos_referencia": "sum",
            "posicao_media": "mean",
        })
        .reset_index()
        .rename(columns={
            "marca_display": "Marca",
            "trafego_organico": "Tráfego",
            "palavras_chave_organicas": "Palavras-chave",
            "backlinks": "Backlinks",
            "dominos_referencia": "Domínios Ref.",
            "posicao_media": "Posição Média",
        })
    )

    col_a, col_b = st.columns([0.8, 0.2])
    with col_b:
        download_csv_button(metricas, "metricas_consolidadas.csv", "Exportar CSV", key="dl_metricas")

    st.dataframe(
        metricas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tráfego": st.column_config.NumberColumn("Tráfego", format="%d"),
            "Palavras-chave": st.column_config.NumberColumn("Palavras-chave", format="%d"),
            "Backlinks": st.column_config.NumberColumn("Backlinks", format="%d"),
            "Domínios Ref.": st.column_config.NumberColumn("Domínios Ref.", format="%d"),
            "Posição Média": st.column_config.NumberColumn("Posição Média", format="%.2f"),
        },
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
<span class="badge">Posição média mais próxima de 1 indica melhor ranqueamento</span>
<span class="badge">Autoridade alta + tráfego baixo = oportunidade de otimização</span>
""",
        unsafe_allow_html=True,
    )

    card_end()

# =========================
# NOTAS TÉCNICAS
# =========================
with st.expander("Notas Técnicas", expanded=False):
    st.markdown(
        """
**Performance:**
- Cache de dados com `@st.cache_data` para otimização de carregamento
- Processamento eficiente de múltiplos arquivos JSON

**Funcionalidades:**
- Filtros dinâmicos por visão e marcas específicas
- Exportação de dados em CSV
- Gráficos interativos com Plotly
- Análise de quadrantes para identificação de oportunidades

**Análise:**
- Identificação automática de oportunidades (alta autoridade, baixo tráfego)
- Comparação competitiva multi-dimensional
- Métricas consolidadas e detalhadas
"""
    )
