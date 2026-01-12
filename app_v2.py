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
# THEME (USER TOGGLE) + CSS
# =========================
LIGHT_THEME_CSS = """
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
  --shadow-md: 0 6px 14px rgba(50, 50, 93, 0.10), 0 2px 6px rgba(0, 0, 0, 0.08);

  --radius-md: 10px;
  --radius-lg: 14px;
}

.stApp{
  background: radial-gradient(800px 520px at 12% 5%, rgba(84,105,212,0.12), transparent 55%),
              radial-gradient(780px 500px at 92% 10%, rgba(14,165,233,0.10), transparent 60%),
              linear-gradient(135deg, #f6f8fa 0%, #fafbfc 100%);
  color: var(--text-primary);
}

.block-container{
  padding-top: 1.2rem;
  max-width: 1400px;
}

a{ color: var(--accent-primary); text-decoration:none; }
a:hover{ color: var(--accent-secondary); }

/* Header */
.dashboard-header{
  text-align:center;
  margin-bottom: 1.0rem;
}
.dashboard-title{
  font-size: 2rem;
  font-weight: 850;
  color: var(--text-primary);
  margin: 0 0 .35rem 0;
  letter-spacing: -0.02em;
}
.dashboard-subtitle{
  color: var(--text-secondary);
  font-size: .95rem;
  font-weight: 450;
  margin:0;
}
.dashboard-meta{
  color: var(--text-tertiary);
  font-size: .82rem;
  margin-top: .55rem;
}

/* Section header */
.section-header{
  display:flex;
  align-items:center;
  gap:.75rem;
  margin-bottom: 1rem;
  padding-bottom: .75rem;
  border-bottom: 2px solid var(--border-light);
}
.section-dot{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  box-shadow: 0 0 0 6px rgba(84,105,212,0.08);
}
.section-title{
  font-size: 1.05rem;
  font-weight: 780;
  color: var(--text-primary);
  margin: 0;
}
.section-desc{
  color: var(--text-secondary);
  font-size: .875rem;
  margin-left:auto;
}

/* Metric cards (HTML) */
.metric-grid{
  display:grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}
.metric-card{
  background: rgba(255,255,255,0.92);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 1.15rem;
  box-shadow: var(--shadow-sm);
  transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
  position: relative;
  overflow:hidden;
}
.metric-card:hover{
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: rgba(14,165,233,0.25);
}
.metric-card::after{
  content:"";
  position:absolute;
  left:0; right:0; bottom:0;
  height:3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  opacity:0;
  transition: opacity .16s ease;
}
.metric-card:hover::after{ opacity:1; }

.metric-label{
  font-size: .78rem;
  font-weight: 700;
  color: var(--text-secondary);
  letter-spacing: .06em;
  text-transform: uppercase;
  margin-bottom: .45rem;
}
.metric-value{
  font-size: 1.65rem;
  font-weight: 860;
  color: var(--text-primary);
  margin-bottom: .2rem;
  line-height: 1.05;
}
.metric-delta{ font-size: .86rem; color: var(--text-tertiary); }
.metric-hint{ font-size: .80rem; color: rgba(26,31,54,.55); margin-top: .2rem; }

/* Chips */
.chip{
  display:inline-flex;
  align-items:center;
  gap:.45rem;
  padding: .42rem .85rem;
  border-radius: 999px;
  font-size: .80rem;
  font-weight: 650;
  border: 1px solid var(--border-light);
  background: rgba(246,248,250,0.95);
  color: var(--text-secondary);
  margin-right: .5rem;
  margin-bottom: .5rem;
  transition: transform .14s ease, border-color .14s ease, box-shadow .14s ease;
}
.chip:hover{
  transform: translateY(-1px);
  border-color: rgba(84,105,212,0.28);
  box-shadow: var(--shadow-sm);
}
.chip-primary{
  background: rgba(84,105,212,0.10);
  border-color: rgba(84,105,212,0.22);
  color: var(--accent-primary);
}

/* Containers border=True (Streamlit) */
div[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius: var(--radius-lg) !important;
  border-color: rgba(227,232,238,0.9) !important;
  background: rgba(255,255,255,0.82) !important;
  box-shadow: var(--shadow-sm) !important;
  transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{
  transform: translateY(-1px);
  box-shadow: var(--shadow-md) !important;
  border-color: rgba(84,105,212,0.22) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{
  gap: .5rem;
  background: rgba(246,248,250,0.95);
  padding: .25rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
}
.stTabs [data-baseweb="tab"]{
  background: transparent;
  border: none;
  border-radius: 8px;
  padding: .6rem 1.2rem;
  color: var(--text-secondary);
  font-weight: 700;
  transition: all .16s ease;
}
.stTabs [aria-selected="true"]{
  background: rgba(255,255,255,0.95);
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
}

/* Buttons */
.stButton > button, .stDownloadButton > button{
  border-radius: 10px !important;
  border: 1px solid var(--border-default) !important;
  background: rgba(255,255,255,0.95) !important;
  color: var(--text-primary) !important;
  font-weight: 750 !important;
  padding: .62rem 1.15rem !important;
  transition: all .16s ease !important;
  box-shadow: var(--shadow-sm) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover{
  background: rgba(246,248,250,0.95) !important;
  border-color: rgba(84,105,212,0.35) !important;
  transform: translateY(-1px) !important;
  box-shadow: var(--shadow-md) !important;
}

/* DataFrames */
div[data-testid="stDataFrame"]{
  border-radius: var(--radius-lg) !important;
  border: 1px solid var(--border-light) !important;
  overflow: hidden !important;
  box-shadow: var(--shadow-sm) !important;
}

@media (max-width: 768px){
  .dashboard-title{ font-size: 1.55rem; }
  .section-desc{ display:none; }
}
</style>
"""

DARK_THEME_CSS = """
<style>
:root{
  --bg-primary: #070a14;
  --bg-secondary: #0f1630;
  --bg-tertiary: #121b3b;

  --text-primary: #eaf0ff;
  --text-secondary: rgba(234,240,255,0.80);
  --text-tertiary: rgba(234,240,255,0.60);

  --border-light: rgba(234,240,255,0.12);
  --border-default: rgba(234,240,255,0.18);

  --accent-primary: #7c7cff;
  --accent-secondary: #22d3ee;

  --shadow-sm: 0 2px 8px rgba(0,0,0,0.45);
  --shadow-md: 0 14px 30px rgba(0,0,0,0.55);

  --radius-md: 10px;
  --radius-lg: 14px;
}

.stApp{
  background: radial-gradient(900px 600px at 10% 0%, rgba(124,124,255,0.24), transparent 55%),
              radial-gradient(900px 600px at 95% 5%, rgba(34,211,238,0.18), transparent 60%),
              linear-gradient(135deg, #050712 0%, #070a14 100%);
  color: var(--text-primary);
}

.block-container{ padding-top: 1.2rem; max-width: 1400px; }

a{ color: var(--accent-secondary) !important; text-decoration:none; }
a:hover{ color: #a5f3fc !important; }

.dashboard-title{ color: var(--text-primary); }
.dashboard-subtitle{ color: var(--text-secondary); }
.dashboard-meta{ color: var(--text-tertiary); }

.section-header{ border-bottom: 2px solid rgba(234,240,255,0.08); }
.section-title{ color: var(--text-primary); }
.section-desc{ color: var(--text-secondary); }
.section-dot{
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  box-shadow: 0 0 0 6px rgba(124,124,255,0.10);
}

/* Metric cards */
.metric-card{
  background: rgba(15,22,48,0.86);
  border: 1px solid rgba(234,240,255,0.10);
  box-shadow: var(--shadow-sm);
}
.metric-label{ color: rgba(234,240,255,0.78); }
.metric-value{ color: var(--text-primary); }
.metric-delta{ color: rgba(234,240,255,0.60); }
.metric-hint{ color: rgba(234,240,255,0.50); }

/* Chips */
.chip{
  border: 1px solid rgba(234,240,255,0.10);
  background: rgba(18,27,59,0.72);
  color: rgba(234,240,255,0.74);
}
.chip-primary{
  background: rgba(124,124,255,0.18);
  border-color: rgba(124,124,255,0.30);
  color: #c7d2fe;
}

/* Containers border=True */
div[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius: var(--radius-lg) !important;
  border-color: rgba(234,240,255,0.12) !important;
  background: rgba(15,22,48,0.72) !important;
  box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{
  box-shadow: var(--shadow-md) !important;
  border-color: rgba(34,211,238,0.22) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{
  background: rgba(18,27,59,0.72);
  border: 1px solid rgba(234,240,255,0.10);
}
.stTabs [data-baseweb="tab"]{ color: rgba(234,240,255,0.75); }
.stTabs [aria-selected="true"]{
  background: rgba(15,22,48,0.88);
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
}

/* Buttons */
.stButton > button, .stDownloadButton > button{
  border: 1px solid rgba(234,240,255,0.16) !important;
  background: rgba(15,22,48,0.90) !important;
  color: var(--text-primary) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover{
  border-color: rgba(34,211,238,0.28) !important;
  background: rgba(18,27,59,0.90) !important;
}

/* Inputs (select/multiselect) */
div[data-baseweb="select"] > div{
  background: rgba(15,22,48,0.90) !important;
  border-color: rgba(234,240,255,0.16) !important;
}
div[data-baseweb="select"] span{
  color: rgba(234,240,255,0.90) !important;
}

/* Slider text */
div[data-testid="stSlider"] *{
  color: rgba(234,240,255,0.85) !important;
}
</style>
"""

def apply_theme(theme_name: str):
    st.markdown(LIGHT_THEME_CSS if theme_name == "Claro" else DARK_THEME_CSS, unsafe_allow_html=True)

if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "Claro"

apply_theme(st.session_state.ui_theme)

# =========================
# UI HELPERS
# =========================
def section_header(title: str, desc: str = ""):
    st.markdown(
        f"""
<div class="section-header">
  <div class="section-dot"></div>
  <h3 class="section-title">{title}</h3>
  {f'<span class="section-desc">{desc}</span>' if desc else ''}
</div>
""",
        unsafe_allow_html=True,
    )

def metric_card(label: str, value: str, delta: str, hint: str = "", tooltip: str = ""):
    st.markdown(
        f"""
<div class="metric-card" title="{tooltip}">
  <div class="metric-label">{label}</div>
  <div class="metric-value">{value}</div>
  <div class="metric-delta">{delta}</div>
  {f'<div class="metric-hint">{hint}</div>' if hint else ''}
</div>
""",
        unsafe_allow_html=True,
    )

def chip(text: str, primary: bool = False, tooltip: str = ""):
    klass = "chip chip-primary" if primary else "chip"
    st.markdown(f"<span class='{klass}' title='{tooltip}'>{text}</span>", unsafe_allow_html=True)

def format_int_br(x):
    try:
        return f"{int(round(float(x))):,}".replace(",", ".")
    except Exception:
        return "0"

def numeric(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)

def futuristic_plotly(fig, theme_name: str, title=None):
    if theme_name == "Claro":
        fig.update_layout(
            template="plotly_white",
            title=title if title else fig.layout.title,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=55, b=10),
            font=dict(color="#1a1f36", size=13),
            title_font=dict(size=15, color="#1a1f36", family="Arial"),
            colorway=["#5469d4", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444"],
            legend=dict(
                bgcolor="rgba(255,255,255,0.92)",
                bordercolor="rgba(203,210,217,0.5)",
                borderwidth=1,
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1.0,
            ),
            hoverlabel=dict(bgcolor="white", font_size=12, bordercolor="#e3e8ee"),
        )
        fig.update_xaxes(showgrid=True, gridcolor="rgba(227,232,238,0.5)", zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(227,232,238,0.5)", zeroline=False)
    else:
        fig.update_layout(
            template="plotly_dark",
            title=title if title else fig.layout.title,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=55, b=10),
            font=dict(color="#eaf0ff", size=13),
            title_font=dict(size=15, color="#eaf0ff", family="Arial"),
            colorway=["#7c7cff", "#22d3ee", "#34d399", "#fbbf24", "#fb7185"],
            legend=dict(
                bgcolor="rgba(15,22,48,0.85)",
                bordercolor="rgba(234,240,255,0.12)",
                borderwidth=1,
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1.0,
            ),
            hoverlabel=dict(
                bgcolor="rgba(15,22,48,0.95)",
                font_size=12,
                bordercolor="rgba(234,240,255,0.15)",
            ),
        )
        fig.update_xaxes(showgrid=True, gridcolor="rgba(234,240,255,0.10)", zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(234,240,255,0.10)", zeroline=False)
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

def style_table(df: pd.DataFrame, gradient_cols=None, theme_name="Claro"):
    gradient_cols = gradient_cols or []
    sty = df.style

    # Hover row
    sty = sty.set_table_styles(
        [{"selector": "tbody tr:hover", "props": [("filter", "brightness(0.96)"), ("transition", "all .12s ease")]}],
        overwrite=False,
    )

    # Gradient cols
    for c in gradient_cols:
        if c in df.columns:
            try:
                sty = sty.background_gradient(subset=[c], cmap="Blues" if theme_name == "Claro" else "PuBuGn")
            except Exception:
                pass

    return sty

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
    f"""
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
# FILTER BAR (REAL CONTAINER)
# =========================
with st.container(border=True):
    c1, c2, c3, c4, c5 = st.columns([1.25, 2.0, 1.05, 1.25, 0.9])

    # with c1:
    #     st.session_state.ui_theme = st.segmented_control(
    #         "Tema",
    #         options=["Claro", "Escuro"],
    #         default=st.session_state.ui_theme,
    #         key="theme_picker",
    #         help="Alterna o tema da interface.",
    #     )
    #     apply_theme(st.session_state.ui_theme)


    with c2:
        modo = st.segmented_control(
            "Visão",
            options=["Todos", "Só Grupo Líder", "Só Concorrentes"],
            default="Todos",
            key="view_mode",
            help="Filtra o dataset por grupo.",
        )
    
    with c3:
        top_n = st.slider(
            "Top concorrentes",
            3, 15, 5, 1,
            help="Ranking por tráfego orgânico"
        )
    
    with c4:
        marcas = sorted(df_seo["marca_display"].dropna().unique().tolist())
        sel_marcas = st.multiselect(
            "Marcas",
            options=marcas,
            default=[],
            help="Opcional"
        )
    
    # with c5:
    #     st.markdown(
    #         f"""
    # <div style="text-align:right; padding-top: 0.25rem;">
    #   <span class="chip" title="Quantidade de arquivos lidos">🧾 {json_files} arquivos</span><br>
    #   <span class="chip" title="Horário do render">⏱️ {datetime.now().strftime("%d/%m %H:%M")}</span>
    # </div>
    # """,
    #         unsafe_allow_html=True,
    #     )

# Apply filters
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
# RESUMO EXECUTIVO
# =========================
with st.container(border=True):
    section_header("Resumo Executivo", "Indicadores + oportunidades (autoridade alta / tráfego baixo)")

    tmp = df_view.copy()
    tmp["trafego_organico"] = numeric(tmp["trafego_organico"])
    tmp["palavras_chave_organicas"] = numeric(tmp["palavras_chave_organicas"])
    tmp["backlinks"] = numeric(tmp["backlinks"])
    tmp["dominos_referencia"] = numeric(tmp["dominos_referencia"])

    best_traf = tmp.loc[tmp["trafego_organico"].idxmax()] if not tmp.empty else None
    best_kw = tmp.loc[tmp["palavras_chave_organicas"].idxmax()] if not tmp.empty else None
    best_back = tmp.loc[tmp["backlinks"].idxmax()] if not tmp.empty else None

    st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)
    metric_card(
        "Maior tráfego",
        best_traf["marca_display"] if best_traf is not None else "-",
        f"{format_int_br(best_traf['trafego_organico'])} visitas/mês" if best_traf is not None else "-",
        hint="Hover para detalhes",
        tooltip="Marca com maior tráfego orgânico estimado no recorte atual",
    )
    metric_card(
        "Maior cobertura",
        best_kw["marca_display"] if best_kw is not None else "-",
        f"{format_int_br(best_kw['palavras_chave_organicas'])} keywords" if best_kw is not None else "-",
        hint="Proxy de presença",
        tooltip="Marca com maior número de palavras-chave orgânicas",
    )
    metric_card(
        "Maior autoridade",
        best_back["marca_display"] if best_back is not None else "-",
        f"{format_int_br(best_back['backlinks'])} backlinks" if best_back is not None else "-",
        hint="Autoridade ≠ tráfego",
        tooltip="Marca com maior volume de backlinks",
    )
    metric_card(
        "Total (recorte)",
        format_int_br(tmp["trafego_organico"].sum()),
        f"{format_int_br(tmp['palavras_chave_organicas'].sum())} keywords • {format_int_br(tmp['backlinks'].sum())} backlinks",
        hint="Mercado filtrado",
        tooltip="Soma dos indicadores no recorte atual",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Quadrantes de oportunidade
    q = tmp[["marca_display", "is_lider", "trafego_organico", "backlinks", "palavras_chave_organicas", "dominio"]].copy()
    traf_med = q["trafego_organico"].median() if not q.empty else 0
    back_med = q["backlinks"].median() if not q.empty else 0

    q["quadrante"] = ""
    q.loc[(q["backlinks"] >= back_med) & (q["trafego_organico"] < traf_med), "quadrante"] = "Oportunidade"
    q.loc[(q["backlinks"] >= back_med) & (q["trafego_organico"] >= traf_med), "quadrante"] = "Líderes"
    q.loc[(q["backlinks"] < back_med) & (q["trafego_organico"] >= traf_med), "quadrante"] = "Alto tráfego"
    q.loc[(q["backlinks"] < back_med) & (q["trafego_organico"] < traf_med), "quadrante"] = "Em desenvolvimento"

    top_op = q[q["quadrante"] == "Oportunidade"].sort_values("backlinks", ascending=False).head(5)

    st.markdown("<br>", unsafe_allow_html=True)
    chip("🎯 Oportunidades", primary=True, tooltip="Backlinks alto + tráfego baixo")
    chip("📌 Quadrante por mediana", tooltip="Heurística: mediana de backlinks e tráfego no recorte")

    if top_op.empty:
        st.caption("Nenhuma oportunidade identificada com os filtros atuais.")
    else:
        left, right = st.columns([0.62, 0.38])

        with left:
            df_op = top_op[["marca_display", "dominio", "backlinks", "trafego_organico", "palavras_chave_organicas"]].copy()
            df_op = df_op.rename(
                columns={
                    "marca_display": "Marca",
                    "dominio": "Domínio",
                    "backlinks": "Backlinks",
                    "trafego_organico": "Tráfego",
                    "palavras_chave_organicas": "Palavras-chave",
                }
            )
            st.dataframe(
                style_table(df_op, gradient_cols=["Backlinks", "Tráfego", "Palavras-chave"], theme_name=st.session_state.ui_theme),
                use_container_width=True,
                hide_index=True,
                height=260,
            )

        with right:
            fig_op = px.bar(
                df_op.sort_values("Backlinks", ascending=True),
                x="Backlinks",
                y="Marca",
                orientation="h",
                title="Oportunidades (Backlinks)",
            )
            fig_op = futuristic_plotly(fig_op, st.session_state.ui_theme)
            st.plotly_chart(fig_op, use_container_width=True)

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["Visão Geral", "Análise Competitiva"])

# =========================
# TAB 1
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

    with st.container(border=True):
        section_header("Indicadores do Grupo Líder", "Cards interativos + leitura rápida")

        st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)
        metric_card("Tráfego Orgânico", format_int_br(trafego_lider), "visitas/mês", tooltip="Soma do tráfego orgânico do Grupo Líder")
        metric_card("Palavras-chave", format_int_br(palavras_lider), "keywords", tooltip="Soma das keywords orgânicas do Grupo Líder")
        metric_card("Domínios Ref.", format_int_br(dominios_lider), "domínios", tooltip="Soma de domínios de referência do Grupo Líder")
        metric_card("Market Share", f"{share_lider:.1f}%".replace(".", ","), "vs mercado", tooltip="Share estimado do tráfego orgânico do Grupo Líder")
        st.markdown("</div>", unsafe_allow_html=True)

        g = df_seo.copy()
        g["trafego_organico"] = numeric(g["trafego_organico"])
        by_brand = g.groupby("marca_display")["trafego_organico"].sum().sort_values(ascending=False).head(12).reset_index()

        fig_micro = px.line(
            by_brand[::-1],
            x="trafego_organico",
            y="marca_display",
            title="Top 12 marcas por tráfego (visão rápida)",
            labels={"trafego_organico": "Tráfego", "marca_display": "Marca"},
        )
        fig_micro = futuristic_plotly(fig_micro, st.session_state.ui_theme)
        st.plotly_chart(fig_micro, use_container_width=True)

    # Palavras-chave principais
    with st.container(border=True):
        section_header("Principais Palavras-chave (Grupo Líder)", "Tabela mais visual + export + mini gráfico")

        keywords_data = {"Palavra-chave": [], "Volume": [], "Tráfego": [], "Marca": []}
        for _, row in df_lider.iterrows():
            for kw in row.get("top_palavras", []) or []:
                keywords_data["Palavra-chave"].append(kw.get("palavra", ""))
                keywords_data["Volume"].append(kw.get("volume", 0))
                keywords_data["Tráfego"].append(kw.get("trafego", 0))
                keywords_data["Marca"].append(row.get("marca", ""))

        df_keywords = pd.DataFrame(keywords_data)
        if df_keywords.empty:
            st.info("Dados de palavras-chave não disponíveis.")
        else:
            df_keywords["Volume"] = numeric(df_keywords["Volume"])
            df_keywords["Tráfego"] = numeric(df_keywords["Tráfego"])
            df_keywords = df_keywords.sort_values("Volume", ascending=False)

            left, right = st.columns([0.70, 0.30])

            with right:
                download_csv_button(df_keywords, "palavras_chave_grupo_lider.csv", "⬇️ Exportar CSV", key="dl_kw")
                topkw = df_keywords.head(10).copy()
                fig_kw = px.bar(
                    topkw.sort_values("Volume", ascending=True),
                    x="Volume",
                    y="Palavra-chave",
                    orientation="h",
                    title="Top 10 por volume",
                )
                fig_kw = futuristic_plotly(fig_kw, st.session_state.ui_theme)
                st.plotly_chart(fig_kw, use_container_width=True)

            with left:
                show_n = st.slider(
                    "Linhas na tabela",
                    20,
                    min(300, len(df_keywords)),
                    min(80, len(df_keywords)),
                    10,
                    key="kw_rows",
                )
                view = df_keywords.head(show_n).copy()
                st.dataframe(
                    style_table(view, gradient_cols=["Volume", "Tráfego"], theme_name=st.session_state.ui_theme),
                    use_container_width=True,
                    hide_index=True,
                    height=430,
                )

    # Top Concorrentes (recorte atual)
    df_concorrentes = df_view[~df_view["is_lider"]].copy()
    df_concorrentes["trafego_organico"] = numeric(df_concorrentes["trafego_organico"])
    df_concorrentes["palavras_chave_organicas"] = numeric(df_concorrentes["palavras_chave_organicas"])
    df_concorrentes["backlinks"] = numeric(df_concorrentes["backlinks"])
    df_concorrentes["dominos_referencia"] = numeric(df_concorrentes["dominos_referencia"])

    with st.container(border=True):
        section_header(f"Top {top_n} Concorrentes (recorte atual)", "Tabela + gráfico futurista")

        if df_concorrentes.empty:
            st.info("Sem concorrentes para exibir com os filtros atuais.")
        else:
            df_top = df_concorrentes.nlargest(top_n, "trafego_organico").copy()

            tbl = pd.DataFrame(
                {
                    "Marca": df_top["marca_display"],
                    "Domínio": df_top["dominio"],
                    "Tráfego": df_top["trafego_organico"].round(0).astype(int),
                    "Palavras-chave": df_top["palavras_chave_organicas"].round(0).astype(int),
                    "Backlinks": df_top["backlinks"].round(0).astype(int),
                    "Domínios Ref.": df_top["dominos_referencia"].round(0).astype(int),
                }
            )

            left, right = st.columns([0.62, 0.38])

            with right:
                download_csv_button(tbl, "top_concorrentes.csv", "⬇️ Exportar CSV", key="dl_top_conc")
                fig_traf = px.bar(
                    df_top.sort_values("trafego_organico", ascending=True),
                    x="trafego_organico",
                    y="marca_display",
                    orientation="h",
                    title="Tráfego orgânico (Top concorrentes)",
                    labels={"trafego_organico": "Tráfego", "marca_display": "Marca"},
                )
                fig_traf = futuristic_plotly(fig_traf, st.session_state.ui_theme)
                st.plotly_chart(fig_traf, use_container_width=True)

            with left:
                st.dataframe(
                    style_table(tbl, gradient_cols=["Tráfego", "Palavras-chave", "Backlinks"], theme_name=st.session_state.ui_theme),
                    use_container_width=True,
                    hide_index=True,
                    height=320,
                )

    # Participação por marca
    with st.container(border=True):
        section_header("Participação por marca (tráfego × keywords)", "Comparativo com barras agrupadas")

        grouped = (
            df_view.assign(
                trafego_organico=numeric(df_view["trafego_organico"]),
                palavras_chave_organicas=numeric(df_view["palavras_chave_organicas"]),
            )
            .groupby("marca_display")[["trafego_organico", "palavras_chave_organicas"]]
            .sum()
            .reset_index()
            .sort_values("trafego_organico", ascending=False)
        )

        max_brands = min(25, len(grouped))
        n_brands = st.slider(
            "Marcas no gráfico",
            5,
            max_brands if max_brands >= 5 else 5,
            min(12, max_brands) if max_brands >= 5 else 5,
            1,
            key="brands_chart",
        )
        grouped_plot = grouped.head(n_brands)

        fig_mix = px.bar(
            grouped_plot,
            x="marca_display",
            y=["trafego_organico", "palavras_chave_organicas"],
            barmode="group",
            title="Tráfego e Keywords por Marca",
            labels={"value": "Volume", "variable": "Métrica", "marca_display": "Marca"},
        )
        fig_mix = futuristic_plotly(fig_mix, st.session_state.ui_theme)
        st.plotly_chart(fig_mix, use_container_width=True)

# =========================
# TAB 2
# =========================
with tab2:
    with st.container(border=True):
        section_header("Mapa Competitivo", "Backlinks × posição média (bolha = tráfego) • Escala log")

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
            title="Autoridade (Backlinks) vs Ranking (Posição Média)",
            labels={"backlinks": "Backlinks (log)", "posicao_media": "Posição média (↓ melhor)", "is_lider": "Grupo"},
            color_discrete_map={
                True: "#5469d4" if st.session_state.ui_theme == "Claro" else "#7c7cff",
                False: "#f59e0b" if st.session_state.ui_theme == "Claro" else "#fbbf24",
            },
        )
        fig_scatter.update_xaxes(type="log")
        fig_scatter = futuristic_plotly(fig_scatter, st.session_state.ui_theme)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with st.container(border=True):
        section_header("Tabela agregada por marca", "Resumo auditável com export + destaque visual")

        metricas = (
            df_view.assign(
                trafego_organico=numeric(df_view["trafego_organico"]),
                palavras_chave_organicas=numeric(df_view["palavras_chave_organicas"]),
                backlinks=numeric(df_view["backlinks"]),
                dominos_referencia=numeric(df_view["dominos_referencia"]),
                posicao_media=numeric(df_view["posicao_media"]),
            )
            .groupby("marca_display")
            .agg(
                {
                    "trafego_organico": "sum",
                    "palavras_chave_organicas": "sum",
                    "backlinks": "sum",
                    "dominos_referencia": "sum",
                    "posicao_media": "mean",
                }
            )
            .reset_index()
            .rename(
                columns={
                    "marca_display": "Marca",
                    "trafego_organico": "Tráfego Orgânico",
                    "palavras_chave_organicas": "Palavras-chave",
                    "backlinks": "Backlinks",
                    "dominos_referencia": "Domínios Referência",
                    "posicao_media": "Posição Média",
                }
            )
            .sort_values("Tráfego Orgânico", ascending=False)
        )

        c1, c2 = st.columns([0.78, 0.22])
        with c2:
            download_csv_button(metricas, "metricas_competitivas.csv", "⬇️ Exportar CSV", key="dl_metricas")

        st.dataframe(
            style_table(metricas, gradient_cols=["Tráfego Orgânico", "Palavras-chave", "Backlinks"], theme_name=st.session_state.ui_theme),
            use_container_width=True,
            hide_index=True,
            height=420,
        )

        chip("📌 Posição média: menor = melhor", primary=True, tooltip="Quanto menor, melhor o posicionamento")
        chip("🧠 Heurística: autoridade alta + tráfego baixo = oportunidade", tooltip="Regra simples para priorização")

        with st.expander("✨ O que chama atenção de recrutadores (o que este dashboard demonstra)"):
            st.markdown(
                """
- **UX de produto**: tema alternável, containers nativos (sem bugs), cards hover, export.
- **Data storytelling**: resumo executivo + quadrante de oportunidades + comparativos.
- **Boas práticas Streamlit**: cache (`@st.cache_data`), layout responsivo, keys, styling.
- **Análise**: ranking competitivo, métricas agregadas e priorização baseada em sinais.
"""
            )
