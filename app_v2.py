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
# THEME (FORÇADO CLARO + GLASS)
# =========================
st.markdown(
    """
<style>
:root{
  --bg1:#f7f8ff;
  --bg2:#ffffff;
  --bg3:#f6fbff;

  --text:#0f172a;
  --muted:rgba(15,23,42,.62);

  --border:rgba(15,23,42,.10);
  --shadow: 0 12px 32px rgba(2,6,23,.10);

  --purple:#7c3aed;
  --cyan:#06b6d4;
  --orange:#f97316;
  --green:#22c55e;
  --red:#ef4444;
  --indigo:#4f46e5;
}

/* forçar fundo claro e texto escuro */
.stApp{
  background: radial-gradient(900px 520px at 10% 0%, rgba(124,58,237,0.14), transparent 60%),
              radial-gradient(900px 520px at 95% 10%, rgba(6,182,212,0.12), transparent 60%),
              radial-gradient(900px 520px at 50% 95%, rgba(34,197,94,0.10), transparent 60%),
              linear-gradient(180deg, var(--bg1), var(--bg2) 40%, var(--bg3));
  color: var(--text) !important;
}

.block-container { padding-top: 1.15rem; }

/* Sidebar (se existir) */
[data-testid="stSidebar"]{
  background: rgba(255,255,255,0.78) !important;
  border-right: 1px solid var(--border) !important;
}

/* Header */
.h-title{
  font-size: 1.75rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  text-align: center;
  margin: 0.25rem 0 0.15rem 0;
  color: var(--text);
}
.h-sub{
  text-align: center;
  color: var(--muted);
  margin: 0 0 1rem 0;
}

/* Panels */
.panel{
  background: rgba(255,255,255,0.88);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 14px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
}
.panel-tight{ padding: 12px; }

/* Section header */
.section{
  display:flex;
  align-items:flex-start;
  gap:10px;
  margin: 0.15rem 0 0.85rem 0;
}
.dot{
  width: 10px; height: 10px; border-radius: 999px;
  margin-top: 6px;
  box-shadow: 0 0 0 6px rgba(79,70,229,0.10);
}
.section-title{ font-size: 1.06rem; font-weight: 850; color: var(--text); }
.section-desc{ color: var(--muted); font-size: 0.92rem; margin-top: 0.10rem; }

/* Chips */
.chip{
  display:inline-flex;
  gap:8px;
  align-items:center;
  padding:6px 10px;
  border-radius:999px;
  border:1px solid var(--border);
  background: rgba(255,255,255,0.88);
  color: rgba(15,23,42,0.78);
  font-size: 0.82rem;
  margin-right: 8px;
}

/* Metric cards */
.metric-grid{
  display:grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}
@media (max-width: 1100px){
  .metric-grid{ grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 650px){
  .metric-grid{ grid-template-columns: 1fr; }
}

.metric{
  position: relative;
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.82));
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 12px;
  overflow: hidden;
  box-shadow: 0 10px 26px rgba(2,6,23,0.08);
}
.metric:before{
  content:"";
  position:absolute;
  inset:-2px;
  opacity: .55;
  pointer-events:none;
  background: radial-gradient(700px 140px at 18% 0%, rgba(79,70,229,0.35), transparent 58%);
}
.metric.purple:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(124,58,237,0.35), transparent 58%); }
.metric.cyan:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(6,182,212,0.35), transparent 58%); }
.metric.orange:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(249,115,22,0.35), transparent 58%); }
.metric.green:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(34,197,94,0.32), transparent 58%); }
.metric.red:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(239,68,68,0.30), transparent 58%); }
.metric.indigo:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(79,70,229,0.35), transparent 58%); }

.metric-label{ position: relative; z-index:1; font-size:0.80rem; color: var(--muted); }
.metric-value{ position: relative; z-index:1; font-size:1.45rem; font-weight: 950; letter-spacing:-0.02em; margin:2px 0 0 0; color: var(--text); }
.metric-delta{ position: relative; z-index:1; font-size:0.80rem; color: rgba(15,23,42,0.68); margin-top:2px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"]{ gap: 8px; }
.stTabs [data-baseweb="tab"]{
  background: rgba(255,255,255,0.85);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 8px 14px;
  color: rgba(15,23,42,0.75);
}
.stTabs [aria-selected="true"]{
  background: rgba(124,58,237,0.12);
  border: 1px solid rgba(124,58,237,0.26);
  color: rgba(15,23,42,0.92);
}

/* Buttons */
.stButton > button, .stDownloadButton > button{
  border-radius: 14px !important;
  border: 1px solid var(--border) !important;
  background: linear-gradient(180deg, rgba(124,58,237,0.14), rgba(6,182,212,0.10)) !important;
  color: var(--text) !important;
  font-weight: 800 !important;
}

/* Dataframe */
div[data-testid="stDataFrame"]{
  border-radius: 16px !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
  background: rgba(255,255,255,0.92) !important;
}

/* Links */
a { color: var(--indigo) !important; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# UI HELPERS
# =========================
def panel_start(tight: bool = False):
    klass = "panel panel-tight" if tight else "panel"
    st.markdown(f"<div class='{klass}'>", unsafe_allow_html=True)


def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


def section_header(title: str, desc: str = "", color: str = "var(--indigo)"):
    st.markdown(
        f"""
<div class="section">
  <div class="dot" style="background:{color};"></div>
  <div>
    <div class="section-title">{title}</div>
    {f"<div class='section-desc'>{desc}</div>" if desc else ""}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, delta: str, tooltip: str, variant: str = "indigo"):
    cls = variant if variant in {"indigo", "purple", "cyan", "orange", "green", "red"} else "indigo"
    st.markdown(
        f"""
<div class="metric {cls}" title="{tooltip}">
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
    """
    Visual futurista em tema claro:
    - colorway neon (roxo/ciano/laranja/verde)
    - fundo transparente
    - grid sutil
    - legenda em "pill" clara
    """
    fig.update_layout(
        template="plotly_white",
        title=title if title else fig.layout.title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=65, b=10),
        font=dict(color="rgba(15,23,42,0.86)", size=13),
        title_font=dict(size=16, color="rgba(15,23,42,0.95)"),
        colorway=["#7c3aed", "#06b6d4", "#f97316", "#22c55e", "#ef4444", "#4f46e5"],
        legend=dict(
            bgcolor="rgba(255,255,255,0.86)",
            bordercolor="rgba(15,23,42,0.10)",
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
            font_family="Arial",
            bordercolor="rgba(15,23,42,0.10)",
        ),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(15,23,42,0.06)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(15,23,42,0.06)", zeroline=False)
    try:
        fig.update_traces(marker=dict(line=dict(width=0.8, color="rgba(15,23,42,0.20)"), opacity=0.92))
    except Exception:
        pass
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
    """
    Extrai métricas de SEO do arquivo JSON (campo: conteudo).
    """
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            conteudo = data.get("conteudo", "")

            # Extrair grupo e marca do caminho do arquivo
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

            # Extrair domínio
            domain_match = re.search(r"domínio: ([\w\.]+)", conteudo)
            if domain_match:
                metrics["dominio"] = domain_match.group(1)

            # Extrair métricas básicas
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

            # Distribuição de países
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

            # Intenção das palavras-chave
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

            # Palavras-chave mais buscadas
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
st.markdown("<div class='h-title'>SEO Grupo Líder</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='h-sub'>Tema claro • UI moderna • gráficos futuristas • insights automáticos (portfolio-ready)</div>",
    unsafe_allow_html=True,
)

df_seo, json_files = load_seo_data()

if df_seo is None or df_seo.empty:
    st.warning("Nenhum dado de SEO encontrado. Verifique se os arquivos JSON estão no diretório correto.")
    st.stop()

# Flags
df_seo["is_lider"] = df_seo["grupo"].astype(str).str.lower().str.contains("lider")
df_seo["marca_display"] = df_seo.apply(
    lambda x: f"{x['marca']} (Grupo Líder)" if x["is_lider"] else x["marca"], axis=1
)

# =========================
# TOP FILTER BAR (robusto e bonito)
# =========================
panel_start(tight=True)
c1, c2, c3, c4 = st.columns([1.35, 1.55, 1.15, 0.95])

with c1:
    modo = st.segmented_control(
        "Visão",
        options=["Todos", "Só Grupo Líder", "Só Concorrentes"],
        default="Todos",
    )

with c2:
    marcas = sorted(df_seo["marca_display"].dropna().unique().tolist())
    sel_marcas = st.multiselect("Marcas (opcional)", options=marcas, default=[])

with c3:
    top_n = st.slider("Top concorrentes (por tráfego)", 3, 15, 5, 1)

with c4:
    st.markdown(
        f"""
<span class="chip">🧾 JSONs: <b>{json_files}</b></span><br/>
<span class="chip">⏱️ {datetime.now().strftime("%d/%m %H:%M")}</span>
""",
        unsafe_allow_html=True,
    )

panel_end()
st.markdown(" ")

# Apply filters
df_view = df_seo.copy()

if modo == "Só Grupo Líder":
    df_view = df_view[df_view["is_lider"]]
elif modo == "Só Concorrentes":
    df_view = df_view[~df_view["is_lider"]]

if sel_marcas:
    df_view = df_view[df_view["marca_display"].isin(sel_marcas)]

if df_view.empty:
    st.info("Com os filtros atuais, não há dados para exibir.")
    st.stop()

# =========================
# RECRUITER-WOW: RESUMO EXECUTIVO + QUADRANTE OPORTUNIDADE
# =========================
def numeric(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)


panel_start()
section_header(
    "Resumo executivo (auto insights)",
    "Um bloco de leitura rápida para tomada de decisão (e demonstração de produto).",
    color="var(--purple)",
)

trafego_total = float(numeric(df_view["trafego_organico"]).sum())
kw_total = float(numeric(df_view["palavras_chave_organicas"]).sum())
back_total = float(numeric(df_view["backlinks"]).sum())

# melhores
tmp = df_view.copy()
tmp["trafego_organico"] = numeric(tmp["trafego_organico"])
tmp["palavras_chave_organicas"] = numeric(tmp["palavras_chave_organicas"])
tmp["backlinks"] = numeric(tmp["backlinks"])

best_traf = tmp.loc[tmp["trafego_organico"].idxmax()] if not tmp.empty else None
best_kw = tmp.loc[tmp["palavras_chave_organicas"].idxmax()] if not tmp.empty else None
best_back = tmp.loc[tmp["backlinks"].idxmax()] if not tmp.empty else None

i1, i2, i3 = st.columns(3)
with i1:
    st.markdown(
        f"<span class='chip'>🏁 Maior tráfego: <b>{best_traf['marca_display']}</b></span><br/>"
        f"<span class='chip'>↳ {format_int_br(best_traf['trafego_organico'])} visitas/mês</span>",
        unsafe_allow_html=True,
    )
with i2:
    st.markdown(
        f"<span class='chip'>🔎 Maior keywords: <b>{best_kw['marca_display']}</b></span><br/>"
        f"<span class='chip'>↳ {format_int_br(best_kw['palavras_chave_organicas'])} keywords</span>",
        unsafe_allow_html=True,
    )
with i3:
    st.markdown(
        f"<span class='chip'>🔗 Maior backlinks: <b>{best_back['marca_display']}</b></span><br/>"
        f"<span class='chip'>↳ {format_int_br(best_back['backlinks'])} backlinks</span>",
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
<br/>
<span class="chip">📦 Cobertura: <b>{format_int_br(trafego_total)}</b> visitas/mês</span>
<span class="chip">🧠 Keywords: <b>{format_int_br(kw_total)}</b></span>
<span class="chip">🧷 Backlinks: <b>{format_int_br(back_total)}</b></span>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# Quadrante oportunidade: backlinks alto e tráfego baixo
q = tmp[["marca_display", "is_lider", "trafego_organico", "backlinks", "palavras_chave_organicas", "dominio"]].copy()
q["trafego_organico"] = numeric(q["trafego_organico"])
q["backlinks"] = numeric(q["backlinks"])
q["palavras_chave_organicas"] = numeric(q["palavras_chave_organicas"])

traf_med = q["trafego_organico"].median() if not q.empty else 0
back_med = q["backlinks"].median() if not q.empty else 0

q["quadrante"] = "—"
q.loc[(q["backlinks"] >= back_med) & (q["trafego_organico"] < traf_med), "quadrante"] = "Oportunidade (autoridade alta, tráfego baixo)"
q.loc[(q["backlinks"] >= back_med) & (q["trafego_organico"] >= traf_med), "quadrante"] = "Líderes (autoridade alta, tráfego alto)"
q.loc[(q["backlinks"] < back_med) & (q["trafego_organico"] >= traf_med), "quadrante"] = "Tráfego alto (autoridade baixa)"
q.loc[(q["backlinks"] < back_med) & (q["trafego_organico"] < traf_med), "quadrante"] = "Em construção (baixo/baixo)"

top_op = q[q["quadrante"].str.contains("Oportunidade")].sort_values("backlinks", ascending=False).head(5)

st.markdown("**🎯 Top oportunidades (Backlinks alto + Tráfego baixo)**")
if top_op.empty:
    st.caption("Nenhuma marca caiu no quadrante de oportunidade com os filtros atuais.")
else:
    st.dataframe(
        top_op[["marca_display", "dominio", "backlinks", "trafego_organico", "palavras_chave_organicas"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "marca_display": "Marca",
            "dominio": "Domínio",
            "backlinks": st.column_config.NumberColumn("Backlinks", format="%d"),
            "trafego_organico": st.column_config.NumberColumn("Tráfego Orgânico", format="%d"),
            "palavras_chave_organicas": st.column_config.NumberColumn("Palavras-chave", format="%d"),
        },
    )

panel_end()
st.markdown(" ")

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["📊 Visão Geral", "📈 Análise Competitiva"])

# =========================
# TAB 1 — VISÃO GERAL
# =========================
with tab1:
    # KPIs do Grupo Líder (dataset completo)
    df_lider = df_seo[df_seo["is_lider"]].copy()
    df_lider["trafego_organico"] = numeric(df_lider["trafego_organico"])
    df_lider["palavras_chave_organicas"] = numeric(df_lider["palavras_chave_organicas"])
    df_lider["dominos_referencia"] = numeric(df_lider["dominos_referencia"])

    trafego_lider = float(df_lider["trafego_organico"].sum())
    palavras_lider = float(df_lider["palavras_chave_organicas"].sum())
    dominios_lider = float(df_lider["dominos_referencia"].sum())

    trafego_total_all = float(numeric(df_seo["trafego_organico"]).sum())
    share_lider = (trafego_lider / trafego_total_all * 100) if trafego_total_all > 0 else 0

    panel_start()
    section_header(
        "KPIs do Grupo Líder",
        "Cards compactos, arredondados e com destaque de cor (visual de produto).",
        color="var(--indigo)",
    )
    st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)

    metric_card(
        "Tráfego Orgânico Total",
        format_int_br(trafego_lider),
        "visitas/mês",
        "Total de visitas mensais das marcas do Grupo Líder",
        variant="cyan",
    )
    metric_card(
        "Palavras-chave Orgânicas",
        format_int_br(palavras_lider),
        "keywords ranqueadas",
        "Soma de palavras-chave das marcas do Grupo Líder",
        variant="purple",
    )
    metric_card(
        "Domínios de Referência",
        format_int_br(dominios_lider),
        "domínios únicos",
        "Total de domínios que apontam links para o Grupo Líder",
        variant="green",
    )
    metric_card(
        "Share de Tráfego (vs mercado)",
        f"{share_lider:.1f}%".replace(".", ","),
        "Grupo Líder vs concorrentes",
        "Porcentagem do tráfego total que pertence ao Grupo Líder",
        variant="orange",
    )

    st.markdown("</div>", unsafe_allow_html=True)
    panel_end()
    st.markdown(" ")

    # Palavras-chave (Grupo Líder)
    panel_start()
    section_header(
        "Palavras-chave mais buscadas (Grupo Líder)",
        "Top termos que puxam volume — com export para CSV.",
        color="var(--cyan)",
    )

    keywords_data = {"Palavra-chave": [], "Volume de Buscas": [], "% Tráfego": [], "Marca": []}
    for _, row in df_lider.iterrows():
        for kw in row.get("top_palavras", []) or []:
            keywords_data["Palavra-chave"].append(kw.get("palavra", ""))
            keywords_data["Volume de Buscas"].append(kw.get("volume", 0))
            keywords_data["% Tráfego"].append(kw.get("trafego", 0))
            keywords_data["Marca"].append(row.get("marca", ""))

    df_keywords = pd.DataFrame(keywords_data)
    if not df_keywords.empty:
        df_keywords = df_keywords.sort_values("Volume de Buscas", ascending=False)

        cA, cB = st.columns([0.78, 0.22])
        with cB:
            download_csv_button(df_keywords, "grupo_lider_keywords.csv", "⬇️ Baixar CSV", key="dl_keywords")

        st.dataframe(
            df_keywords,
            use_container_width=True,
            hide_index=True,
            height=420,
            column_config={
                "Volume de Buscas": st.column_config.NumberColumn("Volume de Buscas", format="%d"),
                "% Tráfego": st.column_config.NumberColumn("% Tráfego", format="%.2f"),
            },
        )
    else:
        st.info("Não encontrei palavras-chave no campo `top_palavras` das marcas do Grupo Líder.")

    panel_end()
    st.markdown(" ")

    # Top Concorrentes por tráfego (a partir do df_view filtrado)
    df_concorrentes = df_view[~df_view["is_lider"]].copy()
    df_concorrentes["trafego_organico"] = numeric(df_concorrentes["trafego_organico"])
    df_concorrentes["palavras_chave_organicas"] = numeric(df_concorrentes["palavras_chave_organicas"])
    df_concorrentes["backlinks"] = numeric(df_concorrentes["backlinks"])
    df_concorrentes["dominos_referencia"] = numeric(df_concorrentes["dominos_referencia"])

    panel_start()
    section_header(
        f"Top {top_n} concorrentes por tráfego",
        "Ranking prático para comparativo rápido + gráfico neon em tema claro.",
        color="var(--orange)",
    )

    if not df_concorrentes.empty:
        df_top = df_concorrentes.nlargest(top_n, "trafego_organico").copy()

        tbl = pd.DataFrame(
            {
                "Concorrente": df_top["marca_display"],
                "Domínio": df_top["dominio"],
                "Tráfego Orgânico": df_top["trafego_organico"].round(0).astype(int),
                "Palavras-chave": df_top["palavras_chave_organicas"].round(0).astype(int),
                "Backlinks": df_top["backlinks"].round(0).astype(int),
                "Domínios Ref.": df_top["dominos_referencia"].round(0).astype(int),
            }
        )

        cA, cB = st.columns([0.78, 0.22])
        with cB:
            download_csv_button(tbl, "top_concorrentes.csv", "⬇️ Baixar CSV", key="dl_top_conc")

        st.dataframe(
            tbl,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Tráfego Orgânico": st.column_config.NumberColumn("Tráfego Orgânico", format="%d"),
                "Palavras-chave": st.column_config.NumberColumn("Palavras-chave", format="%d"),
                "Backlinks": st.column_config.NumberColumn("Backlinks", format="%d"),
                "Domínios Ref.": st.column_config.NumberColumn("Domínios Ref.", format="%d"),
            },
        )

        st.markdown(" ")

        fig_traf = px.bar(
            df_top,
            x="marca_display",
            y="trafego_organico",
            title="Tráfego Orgânico Mensal — Concorrentes",
            labels={"marca_display": "Marca", "trafego_organico": "Visitas/mês"},
        )
        fig_traf = futuristic_plotly_light(fig_traf)
        st.plotly_chart(fig_traf, use_container_width=True)
    else:
        st.info("Com os filtros atuais, não existem concorrentes para ranquear.")

    panel_end()
    st.markdown(" ")

    # Participação por marca (df_view)
    panel_start()
    section_header(
        "Participação por marca (tráfego × keywords)",
        "Comparação de volume e cobertura de palavras-chave.",
        color="var(--green)",
    )

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
        title="Tráfego e Keywords por Marca",
        labels={"value": "Volume", "variable": "Métrica", "marca_display": "Marca"},
    )
    fig_mix = futuristic_plotly_light(fig_mix)
    st.plotly_chart(fig_mix, use_container_width=True)

    panel_end()

    # Diferenciais técnicos (para recrutador)
    with st.expander("✨ Diferenciais técnicos (para recrutadores)", expanded=False):
        st.markdown(
            """
- **Performance/robustez:** `@st.cache_data` para acelerar a leitura e re-render.
- **UX de produto:** filtros globais, export CSV, cards consistentes, layout responsivo.
- **Análise orientada a decisão:** “Resumo executivo” + quadrante de oportunidades.
- **Boas práticas Streamlit:** `key` em downloads (evita `StreamlitDuplicateElementId`).
- **Data storytelling:** gráficos com estética “neon” em tema claro + hover informativo.
"""
        )

# =========================
# TAB 2 — COMPETITIVO
# =========================
with tab2:
    panel_start()
    section_header(
        "Mapa competitivo: Backlinks × Posição Média",
        "Bolha maior = mais tráfego. Posição menor = melhor. (backlinks em escala log)",
        color="var(--purple)",
    )

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
        labels={
            "backlinks": "Backlinks (log)",
            "posicao_media": "Posição média (↓ melhor)",
            "is_lider": "Grupo",
        },
        color_discrete_map={True: "#7c3aed", False: "#f97316"},
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
        "Posição média: %{y:,.0f}<br>"
        "<extra></extra>"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)
    panel_end()
    st.markdown(" ")

    # Tabela agregada
    panel_start()
    section_header(
        "Tabela completa (métricas agregadas por marca)",
        "Resumo por marca com export — ótimo para auditoria e apresentação.",
        color="var(--cyan)",
    )

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
    )

    cA, cB = st.columns([0.78, 0.22])
    with cB:
        download_csv_button(metricas, "metricas_competitivas.csv", "⬇️ Baixar CSV", key="dl_metricas")

    st.dataframe(
        metricas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Tráfego Orgânico": st.column_config.NumberColumn("Tráfego Orgânico", format="%d"),
            "Palavras-chave": st.column_config.NumberColumn("Palavras-chave", format="%d"),
            "Backlinks": st.column_config.NumberColumn("Backlinks", format="%d"),
            "Domínios Referência": st.column_config.NumberColumn("Domínios Referência", format="%d"),
            "Posição Média": st.column_config.NumberColumn("Posição Média", format="%.2f"),
        },
    )

    st.markdown(
        """
<span class="chip">📌 Posição média: quanto mais perto de <b>1</b>, melhor.</span>
<span class="chip">🧠 Dica: “autoridade alta + tráfego baixo” tende a ser o melhor alvo de otimização.</span>
""",
        unsafe_allow_html=True,
    )

    panel_end()
