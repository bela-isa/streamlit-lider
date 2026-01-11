import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
import os
import re

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
# UI THEME (CSS)
# =========================
st.markdown(
    """
<style>
/* --- Base --- */
:root{
  --bg: #0b1220;
  --panel: rgba(255,255,255,0.05);
  --panel2: rgba(255,255,255,0.08);
  --border: rgba(255,255,255,0.10);
  --text: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.65);

  --brand: #7c3aed;   /* roxo */
  --brand2: #22c55e;  /* verde */
  --accent: #f97316;  /* laranja */
  --blue: #38bdf8;
  --danger: #ef4444;
}

.stApp{
  background: radial-gradient(1200px 800px at 10% 0%, rgba(124,58,237,0.20), transparent 60%),
              radial-gradient(1000px 700px at 90% 10%, rgba(34,197,94,0.16), transparent 55%),
              radial-gradient(900px 700px at 50% 90%, rgba(56,189,248,0.12), transparent 60%),
              var(--bg);
  color: var(--text);
}

.block-container { padding-top: 1.4rem; }

/* --- Titles --- */
.h-title{
  font-size: 1.6rem;
  font-weight: 780;
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

/* --- Panels --- */
.panel{
  background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px 14px 10px 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

/* --- Small section header --- */
.section-title{
  display:flex;
  align-items:flex-start;
  gap:10px;
  margin: 0.2rem 0 0.8rem 0;
}
.section-dot{
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--brand);
  box-shadow: 0 0 0 6px rgba(124,58,237,0.12);
  margin-top: 6px;
}
.section-text{
  font-size: 1.05rem;
  font-weight: 750;
}
.section-desc{
  color: var(--muted);
  font-size: 0.92rem;
  margin: 0.15rem 0 0 0;
}

/* --- Metric cards --- */
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

.metric-card{
  position: relative;
  background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 12px 12px 10px 12px;
  overflow: hidden;
}
.metric-card:before{
  content:"";
  position:absolute;
  inset:0;
  background: radial-gradient(600px 120px at 15% 0%, rgba(124,58,237,0.30), transparent 55%);
  opacity: .80;
  pointer-events:none;
}
.metric-card.green:before{
  background: radial-gradient(600px 120px at 15% 0%, rgba(34,197,94,0.28), transparent 55%);
}
.metric-card.orange:before{
  background: radial-gradient(600px 120px at 15% 0%, rgba(249,115,22,0.28), transparent 55%);
}
.metric-card.blue:before{
  background: radial-gradient(600px 120px at 15% 0%, rgba(56,189,248,0.26), transparent 55%);
}
.metric-label{
  position: relative;
  z-index: 1;
  font-size: 0.80rem;
  color: var(--muted);
  margin-bottom: 2px;
}
.metric-value{
  position: relative;
  z-index: 1;
  font-size: 1.45rem;
  font-weight: 850;
  letter-spacing: -0.02em;
  margin: 0;
}
.metric-delta{
  position: relative;
  z-index: 1;
  font-size: 0.80rem;
  color: rgba(255,255,255,0.72);
  margin-top: 2px;
}

/* --- Tabs --- */
.stTabs [data-baseweb="tab-list"]{ gap: 8px; }
.stTabs [data-baseweb="tab"]{
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 999px;
  padding: 8px 14px;
  color: rgba(255,255,255,0.75);
}
.stTabs [aria-selected="true"]{
  background: rgba(124,58,237,0.20);
  border: 1px solid rgba(124,58,237,0.40);
  color: rgba(255,255,255,0.95);
}

/* --- Dataframe container --- */
div[data-testid="stDataFrame"]{
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.10);
}

/* --- Markdown links --- */
a { color: #a78bfa !important; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# UI HELPERS
# =========================
def metric_with_tooltip(label, value, delta, tooltip, variant="purple"):
    variant_class = {
        "purple": "",
        "green": "green",
        "orange": "orange",
        "blue": "blue",
    }.get(variant, "")
    st.markdown(
        f"""
    <div class="metric-card {variant_class}" title="{tooltip}">
        <div class="metric-label">{label}</div>
        <p class="metric-value">{value}</p>
        <div class="metric-delta">{delta}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def section_header(title, desc="", dot_color="var(--brand)"):
    st.markdown(
        f"""
    <div class="section-title">
      <div class="section-dot" style="background:{dot_color};"></div>
      <div>
        <div class="section-text">{title}</div>
        {"<div class='section-desc'>"+desc+"</div>" if desc else ""}
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def panel_start():
    st.markdown("<div class='panel'>", unsafe_allow_html=True)


def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


def apply_plotly_darkglass(fig, title=None):
    fig.update_layout(
        title=title if title is not None else fig.layout.title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=55, b=10),
        font=dict(color="rgba(255,255,255,0.85)"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
        ),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


# =========================
# DATA EXTRACTION
# =========================
def extract_seo_metrics(json_path):
    """
    Extrai métricas de SEO do arquivo JSON.
    Espera um campo "conteudo" no JSON, contendo o texto da análise.
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


def load_seo_data():
    base_dir = "analise-performance"
    all_data = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json") and "analise_detalhada" in file:
                json_path = os.path.join(root, file)
                metrics = extract_seo_metrics(json_path)
                if metrics:
                    all_data.append(metrics)

    return pd.DataFrame(all_data)


# =========================
# HEADER
# =========================
st.markdown("<div class='h-title'>SEO Grupo Líder</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='h-sub'>Painel comparativo de performance orgânica • SEMrush (últimos 12 meses)</div>",
    unsafe_allow_html=True,
)

# =========================
# LOAD
# =========================
df_seo = load_seo_data()

# =========================
# HELPERS: formatting
# =========================
def format_br(value):
    if isinstance(value, float):
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if isinstance(value, int):
        return f"{value:,}".replace(",", ".")
    return value


def style_keywords_df(df):
    # df esperado: Palavra-chave, Volume de Buscas, % Tráfego, Marca
    return (
        df.style.format(
            {
                "Volume de Buscas": lambda x: f"{int(x):,}".replace(",", ".") if pd.notna(x) else "",
                "% Tráfego": lambda x: f"{float(x):.2f}%".replace(".", ",") if pd.notna(x) else "",
            }
        )
        .hide(axis="index")
    )


# =========================
# MAIN
# =========================
if df_seo is None or df_seo.empty:
    st.warning("Nenhum dado de SEO encontrado. Verifique se os arquivos JSON estão no diretório correto.")
    st.stop()

# Flags e display
df_seo["is_lider"] = df_seo["grupo"].astype(str).str.lower().str.contains("lider")
df_seo["marca_display"] = df_seo.apply(
    lambda x: f"{x['marca']} (Grupo Líder)" if x["is_lider"] else x["marca"], axis=1
)

tab1, tab2 = st.tabs(["📊 Visão Geral", "📈 Análise Competitiva"])

# =========================
# TAB 1
# =========================
with tab1:
    # ---- Métricas Grupo Líder
    df_lider = df_seo[df_seo["is_lider"]]
    trafego_lider = float(df_lider["trafego_organico"].sum())
    palavras_lider = float(df_lider["palavras_chave_organicas"].sum())
    dominios_lider = float(df_lider["dominos_referencia"].sum())

    trafego_total = float(df_seo["trafego_organico"].sum())
    share_lider = (trafego_lider / trafego_total * 100) if trafego_total > 0 else 0

    panel_start()
    section_header(
        "Métricas do Grupo Líder",
        "Indicadores consolidados das marcas do Grupo Líder (visão macro).",
        dot_color="var(--brand)",
    )

    st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)
    metric_with_tooltip(
        "Tráfego Orgânico Total",
        f"{trafego_lider:,.0f}".replace(",", "."),
        "Visitas/mês",
        "Total de visitas mensais das marcas do Grupo Líder",
        variant="blue",
    )
    metric_with_tooltip(
        "Palavras-chave Orgânicas",
        f"{palavras_lider:,.0f}".replace(",", "."),
        "Total de palavras-chave",
        "Soma de palavras-chave das marcas do Grupo Líder",
        variant="purple",
    )
    metric_with_tooltip(
        "Domínios de Referência",
        f"{dominios_lider:,.0f}".replace(",", "."),
        "Domínios únicos",
        "Total de domínios que linkam para as marcas do Grupo Líder",
        variant="green",
    )
    metric_with_tooltip(
        "Share de Tráfego",
        f"{share_lider:.1f}%".replace(".", ","),
        "Grupo Líder vs Concorrentes",
        "Porcentagem do tráfego total que pertence ao Grupo Líder",
        variant="orange",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    panel_end()

    st.markdown(" ")

    # ---- Palavras-chave mais buscadas (Grupo Líder)
    panel_start()
    section_header(
        "Palavras-chave mais buscadas",
        "Principais termos que direcionam tráfego para os sites do Grupo Líder (ordenadas por volume).",
        dot_color="var(--blue)",
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
        st.dataframe(
            style_keywords_df(df_keywords),
            use_container_width=True,
            hide_index=True,
            height=420,
        )
    else:
        st.info("Não encontrei palavras-chave no campo `top_palavras` das marcas do Grupo Líder.")
    panel_end()

    st.markdown(" ")

    # ---- Top 5 Concorrentes
    df_concorrentes = df_seo[~df_seo["is_lider"]]

    panel_start()
    section_header(
        "Top 5 concorrentes por tráfego",
        "Ranking por tráfego orgânico mensal estimado + sinais de autoridade.",
        dot_color="var(--accent)",
    )

    if not df_concorrentes.empty:
        df_top5 = df_concorrentes.nlargest(5, "trafego_organico")

        metricas_reais = pd.DataFrame(
            {
                "Concorrente": df_top5["marca"],
                "Domínio": df_top5["dominio"],
                "Tráfego Orgânico": df_top5["trafego_organico"].round(0).astype(int),
                "Palavras-chave": df_top5["palavras_chave_organicas"].round(0).astype(int),
                "Backlinks": df_top5["backlinks"].round(0).astype(int),
                "Domínios Referência": df_top5["dominos_referencia"].round(0).astype(int),
            }
        )

        st.dataframe(
            metricas_reais,
            column_config={
                "Tráfego Orgânico": st.column_config.NumberColumn(
                    "Tráfego Orgânico", help="Visitas mensais vindas de busca orgânica", format="%d"
                ),
                "Palavras-chave": st.column_config.NumberColumn(
                    "Palavras-chave", help="Total de palavras-chave ranqueadas", format="%d"
                ),
                "Backlinks": st.column_config.NumberColumn("Backlinks", help="Total de backlinks", format="%d"),
                "Domínios Referência": st.column_config.NumberColumn(
                    "Domínios Referência", help="Número de sites únicos que fazem link", format="%d"
                ),
            },
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(" ")

        fig_trafego = px.bar(
            df_top5,
            x="marca",
            y=["trafego_organico"],
            title="Tráfego Orgânico Mensal (Top 5)",
            labels={"trafego_organico": "Visitas Mensais", "marca": "Concorrente"},
        )
        fig_trafego = apply_plotly_darkglass(fig_trafego)
        st.plotly_chart(fig_trafego, use_container_width=True)
    else:
        st.info("Não foram encontrados dados de concorrentes nos arquivos JSON.")

    panel_end()

    st.markdown(" ")

    # ---- Share/Tráfego por marca (todas)
    panel_start()
    section_header(
        "Participação e volume por marca",
        "Comparação de tráfego orgânico e palavras-chave entre marcas (Grupo Líder destacado).",
        dot_color="var(--brand2)",
    )

    df_grouped = df_seo.groupby("marca_display")[["trafego_organico", "palavras_chave_organicas"]].sum().reset_index()

    fig_traffic = px.bar(
        df_grouped,
        x="marca_display",
        y=["trafego_organico", "palavras_chave_organicas"],
        title="Tráfego e Palavras-chave por Marca",
        labels={
            "value": "Volume",
            "variable": "Métrica",
            "marca_display": "Marca",
            "trafego_organico": "Tráfego Orgânico",
            "palavras_chave_organicas": "Palavras-chave",
        },
        barmode="group",
    )
    fig_traffic = apply_plotly_darkglass(fig_traffic)
    st.plotly_chart(fig_traffic, use_container_width=True)

    panel_end()

    st.markdown(" ")

    # ---- Estratégia (expander)
    with st.expander("🎯 Pontos de decisão estratégicos (abrir/fechar)", expanded=False):
        st.markdown(
            """
#### Otimização para buscadores
- **Otimização de conteúdo**
  - Desenvolver conteúdo mais relevante e otimizado para palavras-chave comerciais
  - Aumentar a produção de conteúdo técnico e informativo
  - Melhorar a estrutura de URLs e meta tags

- **Construção de links**
  - Estratégia de aquisição de backlinks de qualidade
  - Parcerias com sites relevantes do setor
  - Conteúdo linkável (infográficos, guias, etc.)

- **Performance técnica**
  - Otimizar velocidade de carregamento das páginas
  - Melhorar experiência móvel (Core Web Vitals)
  - Implementar marcação estruturada para resultados enriquecidos

#### Dispositivos móveis
- **Otimização para móveis**
  - Revisar e melhorar a experiência em dispositivos móveis
  - Implementar design responsivo em todas as páginas
  - Otimizar imagens e recursos para carregamento mais rápido

#### Experiência do usuário
- **Navegação**
  - Simplificar a estrutura de navegação
  - Melhorar a usabilidade em dispositivos móveis
  - Menus e hierarquia mais intuitivos

- **Conteúdo**
  - Jornada do usuário mais clara
  - Melhorar CTAs (chamadas para ação)
"""
        )

# =========================
# TAB 2
# =========================
with tab2:
    panel_start()
    section_header(
        "Relação entre backlinks e posição média",
        "Bolhas maiores indicam mais tráfego orgânico. Quanto menor a posição média, melhor.",
        dot_color="var(--accent)",
    )

    fig_position = px.scatter(
        df_seo,
        x="backlinks",
        y="posicao_media",
        size="trafego_organico",
        color="is_lider",
        hover_data=["marca_display", "dominio"],
        title="Backlinks × Posição Média (tamanho = tráfego)",
        labels={
            "backlinks": "Número de Backlinks",
            "posicao_media": "Posição Média",
            "trafego_organico": "Tráfego Orgânico",
            "is_lider": "Empresa",
        },
        color_discrete_map={
            True: "#7c3aed",   # roxo
            False: "#f97316",  # laranja
        },
    )

    # Legenda mais clara
    # (Plotly cria traces em ordem False/True dependendo do dataset — então renomeia se existirem)
    if len(fig_position.data) >= 2:
        # tenta mapear pelo name atual (True/False)
        for tr in fig_position.data:
            if tr.name in ("True", True):
                tr.name = "Grupo Líder"
            elif tr.name in ("False", False):
                tr.name = "Concorrentes"

    fig_position.update_xaxes(type="log", tickformat=",.0f")
    fig_position.update_traces(marker=dict(line=dict(width=1, color="rgba(255,255,255,0.35)")))

    fig_position = apply_plotly_darkglass(fig_position)

    # Template de hover melhor
    fig_position.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>"
        "Domínio: %{customdata[1]}<br>"
        "Backlinks: %{x:,.0f}<br>"
        "Posição Média: %{y:,.0f}<br>"
        "Tráfego Orgânico: %{marker.size:,.0f}<br>"
        "<extra></extra>"
    )

    st.plotly_chart(fig_position, use_container_width=True)
    panel_end()

    st.markdown(" ")

    # ---- Tabela detalhada
    panel_start()
    section_header(
        "Métricas competitivas detalhadas",
        "Resumo por marca (somatórios e média de posição).",
        dot_color="var(--blue)",
    )

    metricas_competitivas = (
        df_seo.groupby("marca_display")
        .agg(
            {
                "trafego_organico": "sum",
                "palavras_chave_organicas": "sum",
                "backlinks": "sum",
                "dominos_referencia": "sum",
                "posicao_media": "mean",
            }
        )
        .round(2)
    )

    metricas_competitivas.columns = [
        "Tráfego Orgânico",
        "Palavras-chave",
        "Backlinks",
        "Domínios Referência",
        "Posição Média",
    ]

    st.dataframe(
        metricas_competitivas.style.format(
            {
                "Tráfego Orgânico": lambda x: f"{x:,.0f}".replace(",", "."),
                "Palavras-chave": lambda x: f"{x:,.0f}".replace(",", "."),
                "Backlinks": lambda x: f"{x:,.0f}".replace(",", "."),
                "Domínios Referência": lambda x: f"{x:,.0f}".replace(",", "."),
                "Posição Média": lambda x: f"{x/1000:.1f}k".replace(".", ",") if x >= 1000 else f"{x:.0f}",
            }
        ),
        use_container_width=True,
    )

    st.markdown(
        """
> **📌 Nota rápida sobre Posição Média**
> - Quanto mais próximo de **1**, melhor o posicionamento.
> - A maior parte do clique acontece na **primeira página** (top 10).
"""
    )

    panel_end()
