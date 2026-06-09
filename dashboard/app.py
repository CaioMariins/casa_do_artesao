"""Dashboard Casa do Artesão - Análise de dados de artesãos."""

import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from folium.plugins import HeatMap
from services.cleaning import limpar_dados
from services.features import criar_colunas_derivadas
from services.loader import carregar_dados
from services.metrics import (
    calclular_metricas,
    calcular_metricas_atuacao,
    calcular_metricas_demograficas,
    calcular_metricas_economicas,
    calcular_metricas_formalizacao,
    calcular_metricas_geograficas,
    calcular_metricas_temporais,
    calcular_metricas_territoriais,
)
from services.normalize import normalizar_dados
from services.validator import validar_consistencia
from streamlit_folium import st_folium

# ============================================================================
# CONFIGURAÇÃO DE TEMAS E ESTILOS
# ============================================================================
COR_FONTE = "#000000"

CORES_GENERO = {
    "Homem": "#4E79A7",
    "Mulher": "#E15759",
    "Outros": "#BAB0AC",
}

COR_PADRAO = "#E09A59"

CORES_PIRAMIDE = {
    "Homem": "#4E79A7",
    "Mulher": "#E15759",
}

CORES_SIM_NAO = {
    "Sim": "#59A14F",
    "Não": "#E15759",
}

CORES_RACA = {
    "branco": "#BACFE6",
    "pardo": "#F28E2B",
    "preto": "#9C755F",
    "amarelo": "#EDC948",
    "indígena": "#59A14F",
    "Não informado": "#BAB0AC",
}
TEMPLATE_PADRAO = "plotly_white"

st.markdown(
    """
<style>
div[data-testid="stMetric"] {
    background: #f3f1e8;
    border: 1px solid #DDE3EA;
    border-radius: 12px;
    padding: 15px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(page_title="Casa do Artesão", layout="wide")
st.title("Dashboard Casa do Artesão")


# ============================================================================
# CARREGAMENTO E PROCESSAMENTO DE DADOS
# ============================================================================
df = carregar_dados()
df = limpar_dados(df)
df = normalizar_dados(df)
df = criar_colunas_derivadas(df)


# ============================================================================
# SIDEBAR - FILTROS
# ============================================================================
st.sidebar.title("Casa do Artesão")

st.sidebar.markdown("---")


filtro_feira = st.sidebar.multiselect(
    "Filtrar por feira", options=df["feira"].unique(), default=df["feira"].unique()
)

filtro_genero = st.sidebar.multiselect(
    "Filtro por gênero", options=df["genero"].unique(), default=df["genero"].unique()
)

filtro_tipo_cadastro = st.sidebar.multiselect(
    "Tipo de cadastro",
    options=df["tipo_cadastro"].unique(),
    default=df["tipo_cadastro"].unique(),
)

filtro_mei = st.sidebar.multiselect(
    "MEI", options=df["mei"].unique(), default=df["mei"].unique()
)

df_filtrado = df[
    (df["feira"].isin(filtro_feira))
    & (df["genero"].isin(filtro_genero))
    & (df["tipo_cadastro"].isin(filtro_tipo_cadastro))
    & (df["mei"].isin(filtro_mei))
]

st.sidebar.metric("Artesãos filtrados", len(df_filtrado))

# ============================================================================
# VALIDAÇÃO DE DADOS
# ============================================================================
erros = validar_consistencia(df)

if erros:
    st.warning("Inconsistências encontradas")
    for erro in erros:
        st.write(erro)
else:
    st.success("Nenhuma inconsistência encontrada")

if df.empty:
    st.error("Dataset vazio")

# ============================================================================
# INDICADORES GERAIS
# ============================================================================
st.header("Indicadores Gerais")

metricas = calclular_metricas(df)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Artesãos", metricas["total_artesaos"])

with col2:
    st.metric("Fixos", metricas["total_fixos"])

with col3:
    st.metric("Visitantes", metricas["total_visitantes"])

with col4:
    st.metric("% MEI", f"{metricas['percentual_mei']:.1f}%")

st.metric("Mulheres no Artesanato", f"{metricas['percentual_mulheres']:.1f}%")

st.divider()


# ============================================================================
# PERFIL DEMOGRÁFICO
# ============================================================================
st.header("Perfil Demográfico")

metricas_demo = calcular_metricas_demograficas(df_filtrado)

metricas_demo["genero"].columns = ["genero", "quantidade"]

# Ordenar por quantidade
metricas_demo["genero"] = metricas_demo["genero"].sort_values(
    "quantidade", ascending=True
)

# Calcular porcentagem
metricas_demo["genero"]["porcentagem"] = (
    metricas_demo["genero"]["quantidade"]
    / metricas_demo["genero"]["quantidade"].sum()
    * 100
).round(1)

maximo = metricas_demo["genero"]["quantidade"].max()

fig_genero = px.bar(
    metricas_demo["genero"],
    x="quantidade",
    y="genero",
    orientation="h",
    title="Distribuição por Gênero",
)

fig_genero.update_traces(
    text=metricas_demo["genero"].apply(
        lambda row: f"{row['porcentagem']}%", axis=1
    ),
    textposition="outside",
    hovertemplate="<b><br>Percentual: %{customdata}%<extra></extra>",
    customdata=metricas_demo["genero"]["porcentagem"],
    marker_color=[CORES_GENERO[g] for g in metricas_demo["genero"]["genero"]],
)
fig_genero.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=12, color=COR_FONTE),
    margin=dict(l=10, r=10, t=40, b=10),
    showlegend=False,
    height=400,
)
fig_genero.update_xaxes(
    range=[0, maximo * 1.25],
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_genero.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)


metricas_demo["raca"].columns = ["raca", "quantidade"]
metricas_demo["raca"] = metricas_demo["raca"].sort_values("quantidade", ascending=True)


# Calcular porcentagem
metricas_demo["raca"]["percentual"] = (
    metricas_demo["raca"]["quantidade"]
    / metricas_demo["raca"]["quantidade"].sum()
    * 100
).round(1)

metricas_demo["raca"]["percentual_texto"] = (
    metricas_demo["raca"]["percentual"].astype(str) + "%"
)
fig_raca = px.bar(
    metricas_demo["raca"],
    x="percentual",
    y="raca",
    orientation="h",
    title="Distribuição por Raça/cor",
)
fig_raca.update_traces(
    text=metricas_demo["raca"]["percentual_texto"],
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Percentual: %{x:.1f}%<extra></extra>",
    marker_color=[CORES_RACA[g] for g in metricas_demo["raca"]["raca"]],
)
fig_raca.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=50, r=20, t=40, b=30),
    showlegend=False,
    height=350,
    xaxis_title="Percentual",
    yaxis_title="",
)

fig_raca.update_xaxes(
    range=[0, 100],
    ticksuffix="%",
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_raca.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)


metricas_demo["faixa_etaria"].columns = ["faixa_etaria", "quantidade"]

df_piramide = df_filtrado[df_filtrado["genero"].isin(["Homem", "Mulher"])]
piramide = (
    df_piramide.groupby(["faixa_etaria", "genero"])
    .size()
    .reset_index(name="quantidade")
)

piramide["quantidade_exibicao"] = piramide["quantidade"].abs()

piramide.loc[piramide["genero"] == "Homem", "quantidade"] *= -1

fig_piramide = px.bar(
    piramide,
    x="quantidade",
    y="faixa_etaria",
    color="genero",
    custom_data=["quantidade_exibicao"],
    orientation="h",
    barmode="relative",
    category_orders={"faixa_etaria": ["18-29", "30-39", "40-49", "50-59", "60+"]},
    title="Pirâmide Etária",
)
fig_piramide.for_each_trace(
    lambda trace: trace.update(marker_color=CORES_PIRAMIDE[trace.name])
)

fig_piramide.update_traces(
    hovertemplate="Faixa: %{y}<br>Quantidade: %{customdata}<extra></extra>",
)
fig_piramide.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=50, r=20, t=40, b=30),
    showlegend=False,
    height=380,
    xaxis_title="Quantidade",
    yaxis_title="Faixa Etária",
)

fig_piramide.update_xaxes(
    tickvals=[-50, -25, 0, 25, 50],
    ticktext=["50", "25", "0", "25", "50"],
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)

fig_piramide.update_yaxes(
    autorange="reversed",
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)

# Adicionar anotações indicando Homem e Mulher
fig_piramide.add_annotation(
    text="<b>Homem</b>",
    x=-50,
    y=1.08,
    xref="x",
    yref="paper",
    showarrow=False,
    font=dict(size=13, color="#FFFFFF"),
)

fig_piramide.add_annotation(
    text="<b>Mulher</b>",
    x=50,
    y=1.08,
    xref="x",
    yref="paper",
    showarrow=False,
    font=dict(size=13, color="#FFFFFF"),
)

col1, espaco, col2 = st.columns([1, 0.1, 1])

with col1:
    st.plotly_chart(fig_genero, use_container_width=True)
with col2:
    st.plotly_chart(fig_raca, use_container_width=True)

st.divider()
st.plotly_chart(fig_piramide, width="stretch")
st.divider()

st.write("### Pessoas com Deficiência")

col1, col2 = st.columns(2)

with col1:
    st.metric("PCD", metricas_demo["pcd"].get("Sim", 0))

with col2:
    st.metric("Não PCD", metricas_demo["pcd"].get("Não", 0))
st.divider()

# ============================================================================
# PERFIL ECONÔMICO
# ============================================================================
st.header("Perfil Econômico")
metricas_economicas = calcular_metricas_economicas(df_filtrado)

metricas_economicas["renda_artesanato"].columns = ["percentual", "quantidade"]

metricas_economicas["renda_artesanato"]["percentual"] = (
    metricas_economicas["renda_artesanato"]["percentual"].astype(str) + "%"
)

maximo = metricas_economicas["renda_artesanato"]["quantidade"].max()

fig_renda = px.bar(
    metricas_economicas["renda_artesanato"],
    x="percentual",
    y="quantidade",
    title="Participação do Artesanato na Renda",
)
fig_renda.update_traces(
    hovertemplate="<b>Percentual: %{x}</b><br><extra></extra>",
    marker_color=COR_PADRAO,
    textposition="outside",
)
fig_renda.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=50, r=20, t=40, b=30),
    showlegend=False,
    height=350,
    xaxis_title="Percentual de Renda",
    yaxis_title="Quantidade",
)
fig_renda.update_xaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)
fig_renda.update_yaxes(
    range=[0, maximo * 1.15],
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)


metricas_economicas["outra_renda"].columns = ["outra_renda", "quantidade"]
metricas_economicas["outra_renda"] = metricas_economicas["outra_renda"].sort_values(
    "quantidade", ascending=True
)

maximo = metricas_economicas["outra_renda"]["quantidade"].max()

# Calcular porcentagem
metricas_economicas["outra_renda"]["porcentagem"] = (
    metricas_economicas["outra_renda"]["quantidade"]
    / metricas_economicas["outra_renda"]["quantidade"].sum()
    * 100
).round(1)

fig_outra_renda = px.bar(
    metricas_economicas["outra_renda"],
    x="quantidade",
    y="outra_renda",
    orientation="h",
    title="Outra Fonte de Renda",
)
fig_outra_renda.update_traces(
    text=metricas_economicas["outra_renda"]["porcentagem"].apply(lambda x: f"{x}%"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Percentual: %{customdata}%<extra></extra>",
    customdata=metricas_economicas["outra_renda"]["porcentagem"],
    marker_color=[
        CORES_SIM_NAO[g] for g in metricas_economicas["outra_renda"]["outra_renda"]
    ],
)
fig_outra_renda.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=120, r=20, t=40, b=10),
    showlegend=False,
    height=350,
    xaxis_title="Quantidade",
    yaxis_title="",
)
fig_outra_renda.update_xaxes(
    range=[0, maximo * 1.15],
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_outra_renda.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)

metricas_economicas["aposentado"].columns = ["aposentado", "quantidade"]
metricas_economicas["aposentado"] = metricas_economicas["aposentado"].sort_values(
    "quantidade", ascending=True
)

maximo = metricas_economicas["aposentado"]["quantidade"].max()

# Calcular porcentagem
metricas_economicas["aposentado"]["porcentagem"] = (
    metricas_economicas["aposentado"]["quantidade"]
    / metricas_economicas["aposentado"]["quantidade"].sum()
    * 100
).round(1)

fig_aposentado = px.bar(
    metricas_economicas["aposentado"],
    x="quantidade",
    y="aposentado",
    orientation="h",
    title="Aposentados",
    color_discrete_sequence=["#27AE60", "#E74C3C"],
)
fig_aposentado.update_traces(
    text=metricas_economicas["aposentado"]["porcentagem"].apply(lambda x: f"{x}%"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Percentual: %{customdata}%<extra></extra>",
    customdata=metricas_economicas["aposentado"]["porcentagem"],
    marker_color=[
        CORES_SIM_NAO[g] for g in metricas_economicas["outra_renda"]["outra_renda"]
    ],
)
fig_aposentado.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=100, r=20, t=40, b=10),
    showlegend=False,
    height=350,
    xaxis_title="Quantidade",
    yaxis_title="",
)
fig_aposentado.update_xaxes(
    range=[0, maximo * 1.15],
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_aposentado.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)

metricas_economicas["pensionista"].columns = ["pensionista", "quantidade"]
metricas_economicas["pensionista"] = metricas_economicas["pensionista"].sort_values(
    "quantidade", ascending=True
)

maximo = metricas_economicas["pensionista"]["quantidade"].max()

# Calcular porcentagem
metricas_economicas["pensionista"]["porcentagem"] = (
    metricas_economicas["pensionista"]["quantidade"]
    / metricas_economicas["pensionista"]["quantidade"].sum()
    * 100
).round(1)

fig_pensionista = px.bar(
    metricas_economicas["pensionista"],
    x="quantidade",
    y="pensionista",
    orientation="h",
    title="Pensionistas",
    color_discrete_sequence=["#3498DB", "#F39C12"],
)
fig_pensionista.update_traces(
    text=metricas_economicas["pensionista"]["porcentagem"].apply(lambda x: f"{x}%"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Percentual: %{customdata}%<extra></extra>",
    customdata=metricas_economicas["pensionista"]["porcentagem"],
    marker_color=[
        CORES_SIM_NAO[g] for g in metricas_economicas["outra_renda"]["outra_renda"]
    ],
)
fig_pensionista.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=100, r=20, t=40, b=10),
    showlegend=False,
    height=350,
    xaxis_title="Quantidade",
    yaxis_title="",
)
fig_pensionista.update_xaxes(
    range=[0, maximo * 1.15],
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_pensionista.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)


col1, espaco, col2 = st.columns([1, 0.1, 1])

with col1:
    st.plotly_chart(fig_renda, use_container_width=True)
with col2:
    st.plotly_chart(fig_outra_renda, use_container_width=True)

st.divider()

col3, espaco, col4 = st.columns([1, 0.1, 1])

with col3:
    st.plotly_chart(fig_aposentado, use_container_width=True)
with col4:
    st.plotly_chart(fig_pensionista, use_container_width=True)

st.divider()
# ============================================================================
# MÉTRICAS TERRITORIAIS
# ============================================================================
st.header("Métricas Territoriais")
metricas_territoriais = calcular_metricas_territoriais(df_filtrado)

metricas_territoriais["feira"].columns = ["feira", "quantidade"]

metricas_territoriais["feira"] = metricas_territoriais["feira"].sort_values(
    "quantidade", ascending=True
)

metricas_territoriais["genero_por_feira"]["percentual"] = (
    metricas_territoriais["genero_por_feira"]["quantidade"]
    / metricas_territoriais["genero_por_feira"]
        .groupby("feira")["quantidade"]
        .transform("sum")  
    * 100
).round(1)

maximo = metricas_territoriais["feira"]["quantidade"].max()

fig_feira = px.bar(
    metricas_territoriais["feira"],
    x="quantidade",
    y="feira",
    orientation="h",
    title="Artesãos por Feira",
)
fig_feira.update_traces(
    hovertemplate="<b>%{y}</b><br>Quantidade: %{x}<extra></extra>",
    marker_color=COR_PADRAO,
)
fig_feira.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=100, r=20, t=40, b=10),
    showlegend=False,
    height=380,
    xaxis_title="Quantidade",
    yaxis_title="",
)
fig_feira.update_xaxes(
    range=[0, maximo * 1.35],
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_feira.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)


fig_genero_feira = px.bar(
    metricas_territoriais["genero_por_feira"],
    x="feira",
    y="percentual",
    color="genero",
    barmode="group",
    custom_data=["percentual"],
    title="Distribuição de Gênero por Feira",
    color_discrete_map=CORES_GENERO,
)
fig_genero_feira.update_traces(
    texttemplate="%{customdata[0]}%",
    textposition="outside",
    hovertemplate=
    "<b>%{x}</b><br>"
    "%{fullData.name}: %{y}<br>"
    "<extra></extra>",
)
fig_genero_feira.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=50, r=20, t=40, b=30),
    height=380,
    xaxis_title="Feira",
    yaxis_title="percentual",
    legend=dict(title="Gênero", orientation="v", x=1.02, y=1),
)
fig_genero_feira.update_xaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)
fig_genero_feira.update_yaxes(
    range=[0, 100],
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
    ticksuffix="%"
)

col1, espaco, col2 = st.columns([1, 0.1, 1])

with col1:
    st.plotly_chart(fig_feira, use_container_width=True)
with col2:
    st.plotly_chart(fig_genero_feira, use_container_width=True)

st.divider()

# ============================================================================
# ATUAÇÃO DOS ARTESÃOS
# ============================================================================
st.header("Atuação dos Artesãos")
metricas_atuacao = calcular_metricas_atuacao(df_filtrado)

metricas_atuacao["tecnicas"].columns = ["tecnica", "quantidade"]
metricas_atuacao["tecnicas"] = metricas_atuacao["tecnicas"].sort_values(
    "quantidade", ascending=True
)

# Calcular porcentagem para técnicas
metricas_atuacao["tecnicas"]["porcentagem"] = (
    metricas_atuacao["tecnicas"]["quantidade"]
    / metricas_atuacao["tecnicas"]["quantidade"].sum()
    * 100
).round(1)


fig_tecnicas = px.bar(
    metricas_atuacao["tecnicas"],
    x="porcentagem",
    y="tecnica",
    orientation="h",
    title="Técnicas Mais Utilizadas",
)
fig_tecnicas.update_traces(
    text=metricas_atuacao["tecnicas"]["porcentagem"].apply(lambda x: f"{x}%"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Percentual: %{x:.1f}%<extra></extra>",
    marker_color=COR_PADRAO,
)
fig_tecnicas.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=80, r=40, t=40, b=10),
    showlegend=False,
    height=400,
    xaxis_title="Percentual",
    yaxis_title="",
)
fig_tecnicas.update_xaxes(
    range=[0, 100],
    ticksuffix="%",
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_tecnicas.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)

metricas_atuacao["produtos"].columns = ["produto", "quantidade"]
metricas_atuacao["produtos"] = metricas_atuacao["produtos"].sort_values(
    "quantidade", ascending=True
)

# Calcular porcentagem para produtos
metricas_atuacao["produtos"]["porcentagem"] = (
    metricas_atuacao["produtos"]["quantidade"]
    / metricas_atuacao["produtos"]["quantidade"].sum()
    * 100
).round(1)

fig_produtos = px.bar(
    metricas_atuacao["produtos"],
    x="porcentagem",
    y="produto",
    orientation="h",
    title="Produtos Mais Produzidos",
)
fig_produtos.update_traces(
    text=metricas_atuacao["produtos"]["porcentagem"].apply(lambda x: f"{x}%"),
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Percentual: %{x:.1f}%<extra></extra>",
    marker_color=COR_PADRAO,
)
fig_produtos.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=80, r=40, t=40, b=10),
    showlegend=False,
    height=400,
    xaxis_title="Percentual",
    yaxis_title="",
)
fig_produtos.update_xaxes(
    range=[0, 100],
    ticksuffix="%",
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_produtos.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)

col3, espaco, col4 = st.columns([1, 0.1, 1])

with col3:
    st.plotly_chart(fig_tecnicas, use_container_width=True)
with col4:
    st.plotly_chart(fig_produtos, use_container_width=True)
st.divider()

# ============================================================================
# FORMALIZAÇÃO (MEI)
# ============================================================================
st.header("Formalização (MEI)")

metricas_formalizacao = calcular_metricas_formalizacao(df_filtrado)

maximo = metricas_formalizacao["mei_por_feira"]["quantidade"].max()

# porcentagem
metricas_formalizacao["mei_por_feira"]["percentual"] = (
    metricas_formalizacao["mei_por_feira"]["quantidade"]
    / metricas_formalizacao["mei_por_feira"]
        .groupby("feira")["quantidade"]
        .transform("sum")    
    * 100
).round(1)

fig_mei = px.bar(
    metricas_formalizacao["mei_por_feira"],
    x="feira",
    y="percentual",
    color="mei",
    barmode="group",
    custom_data=["quantidade"],
    title="MEI por Feira",
    color_discrete_map=CORES_SIM_NAO,
)
fig_mei.update_traces(
    hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:.1f}%<extra></extra>",
)
fig_mei.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=50, r=20, t=40, b=30),
    height=400,
    xaxis_title="Feira",
    yaxis_title="Quantidade",
    legend=dict(title="MEI", orientation="h", x=0.5, y=1.1),
)
fig_mei.update_xaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)
fig_mei.update_yaxes(
    range=[0, 100],
    ticksuffix="%",
    title="Percentual",
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Percentual Geral de MEI", f"{metricas_formalizacao['percentual_mei']:.1f}%"
    )
with col2:
    st.metric("Feira com Mais MEIs", metricas_formalizacao["feira_mais_mei"])
st.divider()

st.plotly_chart(fig_mei, use_container_width=True)

st.divider()

# ============================================================================
# EVOLUÇÃO TEMPORAL
# ============================================================================
st.header("Evolução Temporal")

metricas_temporais = calcular_metricas_temporais(df_filtrado)
metricas_temporais["cadastro_por_mes"]["mes"] = pd.to_datetime(
    metricas_temporais["cadastro_por_mes"]["mes"], format=("%Y-%m")
)

fig_temporal = px.line(
    metricas_temporais["cadastro_por_mes"],
    x="mes",
    y="quantidade",
    markers=True,
    title="Evolução de Cadastros",
    line_shape="spline",
)
fig_temporal.update_traces(
    line=dict(color="#3498DB", width=3),
    marker=dict(size=8, color="#2980B9", symbol="circle"),
    hovertemplate="<b>%{x}</b><br>Cadastros: %{y}<extra></extra>",
    fill="tozeroy",
    fillcolor="rgba(52, 152, 219, 0.2)",
)
fig_temporal.update_layout(
    template=TEMPLATE_PADRAO,
    font=dict(family="Arial, sans-serif", size=11, color=COR_FONTE),
    margin=dict(l=50, r=20, t=40, b=30),
    height=400,
    xaxis_title="Período",
    yaxis_title="Quantidade de Cadastros",
    showlegend=False,
    hovermode="x unified",
)
fig_temporal.update_xaxes(
    dtick="M9",
    tickformat="%b/%Y",
    tickangle=-45,
    tickfont=dict(color=COR_FONTE, size=11),
    title_font=dict(color=COR_FONTE, size=13),
)
fig_temporal.update_yaxes(
    tickfont=dict(color=COR_FONTE, size=11), title_font=dict(color=COR_FONTE, size=13)
)

st.plotly_chart(fig_temporal, use_container_width=True)
st.divider()

# ============================================================================
# DISTRIBUIÇÃO GEOGRÁFICA
# ============================================================================
st.header("Distribuição Geográfica")

metricas_geo = calcular_metricas_geograficas(df)

dados_heatmap = metricas_geo[["latitude", "longitude", "quantidade"]].values.tolist()

mapa = folium.Map(location=[-22.90, -43.20], zoom_start=7, tiles="OpenStreetMap", max_bounds=True,
    min_zoom=3)

fg_marcadores = folium.FeatureGroup(
    name="Marcadores",
    show=True
)

for _, row in metricas_geo.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        radius=row["quantidade"],
        popup=(
            f"""
            Cidade: {row["cidade"]}<br>
            Artesãos: {row["quantidade"]}
            """
        ),
        tooltip=row["cidade"],
        fill=True,
    ).add_to(fg_marcadores)

fg_marcadores.add_to(mapa)

fg_calor = folium.FeatureGroup(name="Mapa de Calor", show=False)
HeatMap(
    dados_heatmap,
    radius=25,
    blur=15,
    max_zoom=10,
).add_to(fg_calor)

fg_calor.add_to(mapa)

folium.LayerControl(collapsed=False).add_to(mapa)

st_folium(mapa, width="stretch", height=500, returned_objects=[])