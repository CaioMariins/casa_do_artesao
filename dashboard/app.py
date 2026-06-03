"""Dashboard Casa do Artesão - Análise de dados de artesãos."""

import folium
import plotly.express as px
import streamlit as st
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
PALETAS_COR = {
    "demografico": ["#FF6B9D", "#C44569", "#4ECDC4", "#44A08D", "#95E1D3"],
    "economico": ["#0066CC", "#003D99", "#004D7A", "#008793", "#00D4FF"],
    "territorial": ["#8B4513", "#D2691E", "#CD853F", "#DAA520", "#FFD700"],
    "atuacao": ["#6C63FF", "#9C89B8", "#DDA15E", "#BC6C25", "#FEFAE0"],
    "formalizacao": ["#2ECC71", "#27AE60", "#F39C12", "#E67E22", "#E74C3C"],
    "temporal": ["#3498DB", "#2980B9", "#34495E", "#95A5A6", "#7F8C8D"],
}

TEMPLATES = {
    "demografico": "plotly",
    "economico": "plotly_white",
    "territorial": "plotly",
    "atuacao": "plotly_white",
    "formalizacao": "plotly",
    "temporal": "plotly_white",
}

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

st.sidebar.metric(
    "Artesãos filtrados",
    len(df_filtrado)
)

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


# ============================================================================
# PERFIL DEMOGRÁFICO
# ============================================================================
st.header("Perfil Demográfico")

metricas_demo = calcular_metricas_demograficas(df_filtrado)

metricas_demo["genero"].columns = ["genero", "quantidade"]

fig_genero = px.pie(
    metricas_demo["genero"],
    names="genero",
    values="quantidade",
    hole=0.4,
    title="Distribuição por Gênero",
    color_discrete_sequence=PALETAS_COR["demografico"],
)
fig_genero.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>",
)
fig_genero.update_layout(
    template=TEMPLATES["demografico"],
    font=dict(family="Arial, sans-serif", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    showlegend=True,
    height=400,
)

metricas_demo["raca"].columns = ["raca", "quantidade"]

fig_raca = px.bar(
    metricas_demo["raca"],
    x="quantidade",
    y="raca",
    orientation="h",
    title="Distribuição por Raça",
    color="quantidade",
    color_continuous_scale="Viridis",
)
fig_raca.update_traces(
    hovertemplate="<b>%{y}</b><br>Quantidade: %{x}<extra></extra>",
)
fig_raca.update_layout(
    template=TEMPLATES["demografico"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=80, r=20, t=40, b=10),
    showlegend=False,
    height=350,
    xaxis_title="Quantidade",
    yaxis_title="",
)

metricas_demo["faixa_etaria"].columns = ["faixa_etaria", "quantidade"]

fig_faixa = px.bar(
    metricas_demo["faixa_etaria"],
    x="faixa_etaria",
    y="quantidade",
    title="Distribuição por Faixa Etária",
    color="quantidade",
    color_continuous_scale="Blues",
)
fig_faixa.update_traces(
    hovertemplate="<b>%{x}</b><br>Quantidade: %{y}<extra></extra>",
)
fig_faixa.update_layout(
    template=TEMPLATES["demografico"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=50, r=20, t=40, b=30),
    showlegend=False,
    height=380,
    xaxis_title="Faixa Etária",
    yaxis_title="Quantidade",
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_genero, use_container_width=True)
with col2:
    st.plotly_chart(fig_raca, use_container_width=True)

st.plotly_chart(fig_faixa, use_container_width=True)

st.write("### Pessoas com Deficiência")

col1, col2 = st.columns(2)

with col1:
    st.metric("PCD", metricas_demo["pcd"].get("Sim", 0))

with col2:
    st.metric("Não PCD", metricas_demo["pcd"].get("Não", 0))


# ============================================================================
# PERFIL ECONÔMICO
# ============================================================================
st.header("Perfil Econômico")
metricas_economicas = calcular_metricas_economicas(df_filtrado)

metricas_economicas["renda_artesanato"].columns = ["percentual", "quantidade"]

fig_renda = px.bar(
    metricas_economicas["renda_artesanato"],
    x="percentual",
    y="quantidade",
    title="Fonte de Renda Principal",
    color_discrete_sequence=PALETAS_COR["economico"],
)
fig_renda.update_traces(
    hovertemplate="<b>%{x}%</b><br>Quantidade: %{y}<extra></extra>",
)
fig_renda.update_layout(
    template=TEMPLATES["economico"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=50, r=20, t=40, b=30),
    showlegend=False,
    height=350,
    xaxis_title="Percentual de Renda",
    yaxis_title="Quantidade",
)

metricas_economicas["outra_renda"].columns = ["outra_renda", "quantidade"]

fig_outra_renda = px.pie(
    metricas_economicas["outra_renda"],
    names="outra_renda",
    values="quantidade",
    hole=0.35,
    title="Outra Fonte de Renda",
    color_discrete_sequence=PALETAS_COR["economico"],
)
fig_outra_renda.update_traces(
    textposition="auto",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>",
)
fig_outra_renda.update_layout(
    template=TEMPLATES["economico"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    showlegend=True,
    height=380,
)

metricas_economicas["aposentado"].columns = ["aposentado", "quantidade"]

fig_aposentado = px.pie(
    metricas_economicas["aposentado"],
    names="aposentado",
    values="quantidade",
    hole=0.35,
    title="Aposentados",
    color_discrete_sequence=["#27AE60", "#E74C3C"],
)
fig_aposentado.update_traces(
    textposition="auto",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>",
)
fig_aposentado.update_layout(
    template=TEMPLATES["economico"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    showlegend=True,
    height=380,
)

metricas_economicas["pensionista"].columns = ["pensionista", "quantidade"]

fig_pensionista = px.pie(
    metricas_economicas["pensionista"],
    names="pensionista",
    values="quantidade",
    hole=0.35,
    title="Pensionistas",
    color_discrete_sequence=["#3498DB", "#F39C12"],
)
fig_pensionista.update_traces(
    textposition="auto",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>",
)
fig_pensionista.update_layout(
    template=TEMPLATES["economico"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    showlegend=True,
    height=380,
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_renda, use_container_width=True)
with col2:
    st.plotly_chart(fig_outra_renda, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig_aposentado, use_container_width=True)
with col4:
    st.plotly_chart(fig_pensionista, use_container_width=True)


# ============================================================================
# MÉTRICAS TERRITORIAIS
# ============================================================================
st.header("Métricas Territoriais")
metricas_territoriais = calcular_metricas_territoriais(df_filtrado)

metricas_territoriais["feira"].columns = ["feira", "quantidade"]

fig_feira = px.bar(
    metricas_territoriais["feira"],
    x="quantidade",
    y="feira",
    orientation="h",
    title="Artesãos por Feira",
    color="quantidade",
    color_continuous_scale="Oranges",
)
fig_feira.update_traces(
    hovertemplate="<b>%{y}</b><br>Quantidade: %{x}<extra></extra>",
)
fig_feira.update_layout(
    template=TEMPLATES["territorial"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=100, r=20, t=40, b=10),
    showlegend=False,
    height=380,
    xaxis_title="Quantidade",
    yaxis_title="",
)

fig_genero_feira = px.bar(
    metricas_territoriais["genero_por_feira"],
    x="feira",
    y="quantidade",
    color="genero",
    barmode="group",
    title="Distribuição de Gênero por Feira",
    color_discrete_sequence=["#FF69B4", "#4169E1"],
)
fig_genero_feira.update_traces(
    hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>",
)
fig_genero_feira.update_layout(
    template=TEMPLATES["territorial"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=50, r=20, t=40, b=30),
    height=380,
    xaxis_title="Feira",
    yaxis_title="Quantidade",
    legend=dict(title="Gênero", orientation="v", x=1.02, y=1),
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_feira, use_container_width=True)
with col2:
    st.plotly_chart(fig_genero_feira, use_container_width=True)


# ============================================================================
# ATUAÇÃO DOS ARTESÃOS
# ============================================================================
st.header("Atuação dos Artesãos")
metricas_atuacao = calcular_metricas_atuacao(df_filtrado)

metricas_atuacao["tecnicas"].columns = ["tecnica", "quantidade"]

fig_tecnicas = px.bar(
    metricas_atuacao["tecnicas"],
    x="quantidade",
    y="tecnica",
    orientation="h",
    title="Técnicas Mais Utilizadas",
    color="quantidade",
    color_continuous_scale="Purples",
)
fig_tecnicas.update_traces(
    hovertemplate="<b>%{y}</b><br>Quantidade: %{x}<extra></extra>",
)
fig_tecnicas.update_layout(
    template=TEMPLATES["atuacao"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=120, r=20, t=40, b=10),
    showlegend=False,
    height=400,
    xaxis_title="Quantidade",
    yaxis_title="",
)

metricas_atuacao["produtos"].columns = ["produto", "quantidade"]

fig_produtos = px.bar(
    metricas_atuacao["produtos"],
    x="quantidade",
    y="produto",
    orientation="h",
    title="Produtos Mais Produzidos",
    color="quantidade",
    color_continuous_scale="RdYlGn",
)
fig_produtos.update_traces(
    hovertemplate="<b>%{y}</b><br>Quantidade: %{x}<extra></extra>",
)
fig_produtos.update_layout(
    template=TEMPLATES["atuacao"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=150, r=20, t=40, b=10),
    showlegend=False,
    height=400,
    xaxis_title="Quantidade",
    yaxis_title="",
)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig_tecnicas, use_container_width=True)
with col4:
    st.plotly_chart(fig_produtos, use_container_width=True)


# ============================================================================
# FORMALIZAÇÃO (MEI)
# ============================================================================
st.header("Formalização (MEI)")

metricas_formalizacao = calcular_metricas_formalizacao(df_filtrado)

fig_mei = px.bar(
    metricas_formalizacao["mei_por_feira"],
    x="feira",
    y="quantidade",
    color="mei",
    barmode="group",
    title="MEI por Feira",
    color_discrete_map={"Sim": "#27AE60", "Não": "#E74C3C"},
)
fig_mei.update_traces(
    hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>",
)
fig_mei.update_layout(
    template=TEMPLATES["formalizacao"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=50, r=20, t=40, b=30),
    height=400,
    xaxis_title="Feira",
    yaxis_title="Quantidade",
    legend=dict(title="MEI", orientation="h", x=0.5, y=1.1),
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Percentual Geral de MEI", f"{metricas_formalizacao['percentual_mei']:.1f}%"
    )
with col2:
    st.metric("Feira com Mais MEIs", metricas_formalizacao["feira_mais_mei"])

st.plotly_chart(fig_mei, use_container_width=True)


# ============================================================================
# EVOLUÇÃO TEMPORAL
# ============================================================================
st.header("Evolução Temporal")

metricas_temporais = calcular_metricas_temporais(df_filtrado)

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
    template=TEMPLATES["temporal"],
    font=dict(family="Arial, sans-serif", size=11),
    margin=dict(l=50, r=20, t=40, b=30),
    height=400,
    xaxis_title="Período",
    yaxis_title="Quantidade de Cadastros",
    showlegend=False,
    hovermode="x unified",
)

st.plotly_chart(fig_temporal, use_container_width=True)


# ============================================================================
# DISTRIBUIÇÃO GEOGRÁFICA
# ============================================================================
st.header("Distribuição Geográfica")

metricas_geo = calcular_metricas_geograficas(df)

mapa = folium.Map(location=[-22.90, -43.20], zoom_start=7, tiles="OpenStreetMap")

for _, row in metricas_geo.iterrows():
    folium.CircleMarker(
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
    ).add_to(mapa)

st_folium(mapa, width="stretch", height=500, returned_objects=[])
