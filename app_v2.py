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
# THEME (LIGHT + GLASS)
# =========================
st.markdown(
    """
<style>
:root{
  --bg: #f6f7fb;
  --bg2: #ffffff;
  --panel: rgba(255,255,255,0.72);
  --panel2: rgba(255,255,255,0.88);
  --border: rgba(15,23,42,0.10);
  --text: rgba(15,23,42,0.92);
  --muted: rgba(15,23,42,0.62);

  --purple: #7c3aed;
  --cyan: #06b6d4;
  --orange: #f97316;
  --green: #22c55e;
  --red: #ef4444;
  --indigo: #4f46e5;

  --shadow: 0 10px 30px rgba(2,6,23,0.10);
}

.stApp{
  background:
    radial-gradient(900px 500px at 10% 0%, rgba(124,58,237,0.16), transparent 60%),
    radial-gradient(850px 480px at 95% 10%, rgba(6,182,212,0.14), transparent 62%),
    radial-gradient(900px 520px at 50% 95%, rgba(34,197,94,0.10), transparent 60%),
    var(--bg);
  color: var(--text);
}

.block-container { padding-top: 1.15rem; }

/* Titles */
.h-title{
  font-size: 1.65rem;
  font-weight: 820;
  letter-spacing: -0.02em;
  text-align: center;
  margin: 0.25rem 0 0.25rem 0;
}
.h-sub{
  text-align: center;
  color: var(--muted);
  margin-top: 0;
  margin-bottom: 1rem;
}

/* Panels */
.panel{
  background: linear-gradient(180deg, var(--panel2), var(--panel));
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 14px 14px 10px 14px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
}

.panel-tight{
  padding: 12px 12px 8px 12px;
}

/* Section header */
.section{
  display:flex;
  align-items:flex-start;
  gap:10px;
  margin: 0.25rem 0 0.85rem 0;
}
.dot{
  width: 10px;
  height: 10px;
  border-radius: 999px;
  margin-top: 6px;
  box-shadow: 0 0 0 6px rgba(79,70,229,0.10);
}
.section-title{
  font-size: 1.06rem;
  font-weight: 780;
}
.section-desc{
  color: var(--muted);
  font-size: 0.92rem;
  margin-top: 0.1rem;
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
  background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(255,255,255,0.72));
  border: 1px solid rgba(15,23,42,0.10);
  border-radius: 18px;
  padding: 12px 12px 10px 12px;
  overflow: hidden;
  box-shadow: 0 10px 26px rgba(2,6,23,0.07);
}
.metric:before{
  content:"";
  position:absolute;
  inset:-2px;
  opacity: .55;
  pointer-events:none;
  background: radial-gradient(700px 140px at 18% 0%, rgba(124,58,237,0.35), transparent 58%);
}
.metric.cyan:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(6,182,212,0.35), transparent 58%); }
.metric.orange:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(249,115,22,0.35), transparent 58%); }
.metric.green:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(34,197,94,0.32), transparent 58%); }
.metric.red:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(239,68,68,0.30), transparent 58%); }
.metric.indigo:before{ background: radial-gradient(700px 140px at 18% 0%, rgba(79,70,229,0.35), transparent 58%); }

.metric-label{
  position: relative;
  z-index: 1;
  font-size: 0.80rem;
  color: var(--muted);
}
.metric-value{
  position: relative;
  z-index: 1;
  font-size: 1.45rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  margin: 2px 0 0 0;
}
.metric-delta{
  position: relative;
  z-index: 1;
  font-size: 0.80rem;
  color: rgba(15,23,42,0.68);
  margin-top: 2px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{ gap: 8px; }
.stTabs [data-baseweb="tab"]{
  background: rgba(255,255,255,0.78);
  border: 1px solid rgba(15,23,42,0.10);
  border-radius: 999px;
  padding: 8px 14px;
  color: rgba(15,23,42,0.75);
}
.stTabs [aria-selected="true"]{
  background: rgba(124,58,237,0.12);
  border: 1px solid rgba(124,58,237,0.28);
  color: rgba(15,23,42,0.92);
}

/* Dataframe */
div[data-testid="stDataFrame"]{
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(15,23,42,0.10);
  background: rgba(255,255,255,0.85);
}

/* Links */
a { color: #4f46e5 !important; }

/* Small chips */
.chip{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(15,23,42,0.10);
  background: rgba(255,255,255,0.82);
  color: rgba(15,23,42,0.80);
  font-size: 0.82rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# UI HELPERS
# =========================
def panel_start(tight=False):
    klass = "panel panel-tight" if tight else "panel"
    st.markdown(f"<div class='{klass}'>", unsafe_allow_html=True)


def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


def section_header(title, desc="", color="var(--indigo)"):
    st.markdown(
        f"""
<div class="section">
  <div class="dot" style="background:{color}; box-shadow: 0 0 0 6px rgba(79,70,229,0.10);"></div>
  <div>
    <div class="section-title">{title}</div>
    {f"<div class='section-desc'>{desc}</div>" if desc else ""}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def metric_card(label, value, delta, tooltip, variant="indigo"):
    cls = {
        "indigo": "indigo",
        "purple": "",
        "cyan": "cyan",
        "orange": "orange",
        "green": "green",
        "red": "red",
    }.get(variant, "indigo")
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


def format_float_br(x, decimals=2):
    try:
        return f"{float(x):,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0"


def apply_plotly_futuristic_light(fig, title=None):
    # “Futurista” sem deixar poluído: neon colorway + grid sutil + fundo transparente
    fig.update_layout(
        title=title if title is not None else fig.layout.title,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=60, b=10),
        font=dict(color="rgba(15,23,42,0.85)", size=13),
        title_font=dict(size=16, color="rgba(15,23,42,0.92)"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.70)",
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
        colorway=["#7c3aed", "#06b6d4", "#f97316", "#22c55e", "#ef4444", "#4f46e5"],
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(15,23,42,0.06)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(15,23,42,0.06)", zeroline=False)

    # Linha “neon” discreta nos traces quando aplicável
    try:
        fig.update_traces(marker=dict(line=dict(width=0.6, color="rgba(15,23,42,0.20)")))
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
# EXTRACTION / LOAD
# =========================
def extract_seo_metrics(json_path):
    """
    Extrai métricas de SEO do arquivo JSON (campo esperado: "conteudo").
    """
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

    df = pd.DataFrame(all_data)
    return df, file_count


# =========================
# HEADER
# =========================
st.markdown("<div class='h-title'>SEO Grupo Líder</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='h-sub'>Dashboard comparativo de performance orgânica • visual premium (tema claro) • dados SEMrush</div>",
    unsafe_allow_html=True,
)

# Load
df_seo, json_files = load_seo_data()

if df_seo is None or df_seo.empty:
    st.warning("Nenhum dado de SEO encontrado. Verifique se os arquivos JSON estão no diretório correto.")
    st.stop()

# Flags e display
df_seo["is_lider"] = df_seo["grupo"].astype(str).str.lower().str.contains("lider")
df_seo["marca_display"] = df_seo.apply(
    lambda x: f"{x['marca']} (Grupo Líder)" if x["is_lider"] else x["marca"], axis=1
)

# =========================
# TOP BAR (filters + info)
# =========================
panel_start(tight=True)
c1, c2, c3, c4 = st.columns([1.3, 1.4, 1.3, 1.0])

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
    top_n = st.slider("Top concorrentes (por tráfego)", min_value=3, max_value=15, value=5, step=1)

with c4:
    st.markdown(
        f"""
<div class="chip">🧾 JSONs lidos: <b>{json_files}</b></div><br/>
<div class="chip">⏱️ Atualizado: <b>{datetime.now().strftime("%d/%m %H:%M")}</b></div>
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
# EXECUTIVE INSIGHTS (recruiter wow)
# =========================
def safe_max_row(df, col):
    if df.empty:
        return None
    df2 = df.copy()
    df2[col] = pd.to_numeric(df2[col], errors="coerce")
    df2 = df2.dropna(subset=[col])
    if df2.empty:
        return None
    return df2.loc[df2[col].idxmax()]


panel_start()
section_header(
    "Resumo executivo (insights automáticos)",
    "Gera conclusões rápidas para tomada de decisão — e mostra robustez do dashboard.",
    color="var(--purple)",
)

trafego_total = float(pd.to_numeric(df_view["trafego_organico"], errors="coerce").fillna(0).sum())
kw_total = float(pd.to_numeric(df_view["palavras_chave_organicas"], errors="coerce").fillna(0).sum())
back_total = float(pd.to_numeric(df_view["backlinks"], errors="coerce").fillna(0).sum())

best_trafego = safe_max_row(df_view, "trafego_organico")
best_kw = safe_max_row(df_view, "palavras_chave_organicas")
best_back = safe_max_row(df_view, "backlinks")

ins_cols = st.columns(3)

with ins_cols[0]:
    st.markdown(
        f"**🏁 Maior tráfego:** {best_trafego['marca_display'] if best_trafego is not None else '—'}"
        f"<br/>↳ {format_int_br(best_trafego['trafego_organico']) if best_trafego is not None else '—'} visitas/mês",
        unsafe_allow_html=True,
    )

with ins_cols[1]:
    st.markdown(
        f"**🔎 Maior volume de keywords:** {best_kw['marca_display'] if best_kw is not None else '—'}"
        f"<br/>↳ {format_int_br(best_kw['palavras_chave_organicas']) if best_kw is not None else '—'} keywords",
        unsafe_allow_html=True,
    )

with ins_cols[2]:
    st.markdown(
        f"**🔗 Maior autoridade (backlinks):** {best_back['marca_display'] if best_back is not None else '—'}"
        f"<br/>↳ {format_int_br(best_back['backlinks']) if best_back is not None else '—'} backlinks",
        unsafe_allow_html=True,
    )

st.markdown("---")

# A “história” que recruta gosta: total + oportunidades
st.markdown(
    f"""
- **Cobertura atual do painel:** {format_int_br(trafego_total)} visitas/mês • {format_int_br(kw_total)} keywords • {format_int_br(back_total)} backlinks  
- **Oportunidade típica (SEO):** marcas com **alto backlink** e **tráfego baixo** → potencial de ganho via conteúdo + otimização técnica.
""",
)

panel_end()
st.markdown(" ")

# =========================
# TABS
# =========================
tab1, tab2 = st.tabs(["📊 Visão Geral", "📈 Análise Competitiva"])

# =========================
# TAB 1
# =========================
with tab1:
    # KPIs do Grupo Líder (sempre calculados do dataset completo, não só do filtro)
    df_lider_all = df_seo[df_seo["is_lider"]]
    trafego_lider = float(pd.to_numeric(df_lider_all["trafego_organico"], errors="coerce").fillna(0).sum())
    palavras_lider = float(pd.to_numeric(df_lider_all["palavras_chave_organicas"], errors="coerce").fillna(0).sum())
    dominios_lider = float(pd.to_numeric(df_lider_all["dominos_referencia"], errors="coerce").fillna(0).sum())

    trafego_total_all = float(pd.to_numeric(df_seo["trafego_organico"], errors="coerce").fillna(0).sum())
    share_lider = (trafego_lider / trafego_total_all * 100) if trafego_total_all > 0 else 0

    panel_start()
    section_header(
        "KPIs do Grupo Líder",
        "Indicadores consolidados (ótimos para opening de apresentação).",
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
        "Total de domínios que apontam links para marcas do Grupo Líder",
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

    # Palavras-chave
    panel_start()
    section_header(
        "Palavras-chave mais buscadas (Grupo Líder)",
        "Top termos que puxam volume — útil para estratégia de conteúdo.",
        color="var(--cyan)",
    )

    keywords_data = {"Palavra-chave": [], "Volume de Buscas": [], "% Tráfego": [], "Marca": []}
    for _, row in df_lider_all.iterrows():
        for kw in row.get("top_palavras", []) or []:
            keywords_data["Palavra-chave"].append(kw.get("palavra", ""))
            keywords_data["Volume de Buscas"].append(kw.get("volume", 0))
            keywords_data["% Tráfego"].append(kw.get("trafego", 0))
            keywords_data["Marca"].append(row.get("marca", ""))

    df_keywords = pd.DataFrame(keywords_data)
    if not df_keywords.empty:
        df_keywords = df_keywords.sort_values("Volume de Buscas", ascending=False)

        # Download (chama atenção: utilidade imediata)
        colA, colB = st.columns([0.75, 0.25])
        with colB:
            download_csv_button(
                df_keywords,
                filename="grupo_lider_keywords.csv",
                label="⬇️ Baixar CSV",
                key="dl_keywords_lider",
            )

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

    # Top concorrentes por tráfego (baseado no df_view ou geral?)
    df_concorrentes = df_view[~df_view["is_lider"]]
    panel_start()
    section_header(
        f"Top {top_n} concorrentes por tráfego",
        "Ranking prático para comparativo rápido + sinais de autoridade.",
        color="var(--orange)",
    )

    if not df_concorrentes.empty:
        df_top = df_concorrentes.nlargest(top_n, "trafego_organico").copy()

        tbl = pd.DataFrame(
            {
                "Concorrente": df_top["marca_display"],
                "Domínio": df_top["dominio"],
                "Tráfego Orgânico": pd.to_numeric(df_top["trafego_organico"], errors="coerce").fillna(0).round(0).astype(int),
                "Palavras-chave": pd.to_numeric(df_top["palavras_chave_organicas"], errors="coerce").fillna(0).round(0).astype(int),
                "Backlinks": pd.to_numeric(df_top["backlinks"], errors="coerce").fillna(0).round(0).astype(int),
                "Domínios Ref.": pd.to_numeric(df_top["dominos_referencia"], errors="coerce").fillna(0).round(0).astype(int),
            }
        )

        cA, cB = st.columns([0.75, 0.25])
        with cB:
            download_csv_button(tbl, "top_concorrentes.csv", "⬇️ Baixar CSV", key="dl_top_concorrentes")

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
        fig_traf.update_traces(
            marker=dict(line=dict(width=0.8, color="rgba(15,23,42,0.25)")),
            opacity=0.92,
        )
        fig_traf = apply_plotly_futuristic_light(fig_traf)
        st.plotly_chart(fig_traf, use_container_width=True)
    else:
        st.info("Com os filtros atuais, não existem concorrentes para ranquear.")

    panel_end()
    st.markdown(" ")

    # Comparativo tráfego x keywords (todas marcas do df_view)
    panel_start()
    section_header(
        "Participação por marca (tráfego × keywords)",
        "Visão de mercado: volume e cobertura de palavras-chave.",
        color="var(--green)",
    )

    grouped = (
        df_view.groupby("marca_display")[["trafego_organico", "palavras_chave_organicas"]]
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
    fig_mix = apply_plotly_futuristic_light(fig_mix)
    st.plotly_chart(fig_mix, use_container_width=True)

    panel_end()

    # Diferenciais técnicos (recrutador)
    with st.expander("✨ Diferenciais técnicos (para recrutadores)", expanded=False):
        st.markdown(
            """
- **Performance/robustez:** uso de `@st.cache_data` para acelerar leitura e processamento.
- **UX de produto:** filtros no topo, downloads, cards consistentes, painéis, layout responsivo.
- **Análise orientada a decisão:** “Resumo executivo” com insights automáticos (melhor tráfego/keywords/backlinks).
- **Boa prática de Streamlit:** `key` nos botões de download (evita erro de IDs duplicados).
- **Design system leve:** tema claro, glassmorphism, cores marcantes sem “poluir”.
"""
        )

# =========================
# TAB 2 — COMPETITIVE
# =========================
with tab2:
    panel_start()
    section_header(
        "Mapa competitivo: Backlinks × Posição Média",
        "Bola maior = mais tráfego. Posição menor = melhor. (escala log em backlinks)",
        color="var(--purple)",
    )

    df_plot = df_view.copy()
    # evita problemas de tipo
    for col in ["backlinks", "posicao_media", "trafego_organico"]:
        df_plot[col] = pd.to_numeric(df_plot[col], errors="coerce").fillna(0)

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
    fig_scatter.update_traces(
        marker=dict(
            line=dict(width=1, color="rgba(15,23,42,0.25)"),
            opacity=0.92,
        )
    )

    # Renomeia legenda
    if len(fig_scatter.data) >= 1:
        for tr in fig_scatter.data:
            if str(tr.name) in ("True", "true"):
                tr.name = "Grupo Líder"
            elif str(tr.name) in ("False", "false"):
                tr.name = "Concorrentes"

    fig_scatter = apply_plotly_futuristic_light(fig_scatter)

    # Hover “premium”
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

    panel_start()
    section_header(
        "Tabela completa (métricas agregadas por marca)",
        "Boa para auditoria e export.",
        color="var(--cyan)",
    )

    metricas = (
        df_view.groupby("marca_display")
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
    )

    metricas.rename(
        columns={
            "marca_display": "Marca",
            "trafego_organico": "Tráfego Orgânico",
            "palavras_chave_organicas": "Palavras-chave",
            "backlinks": "Backlinks",
            "dominos_referencia": "Domínios Referência",
            "posicao_media": "Posição Média",
        },
        inplace=True,
    )

    cA, cB = st.columns([0.75, 0.25])
    with cB:
        download_csv_button(metricas, "metricas_competitivas.csv", "⬇️ Baixar CSV", key="dl_metricas_compet")

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
<div class="chip">📌 Posição média: quanto mais perto de <b>1</b>, melhor.</div>
""",
        unsafe_allow_html=True,
    )

    panel_end()
