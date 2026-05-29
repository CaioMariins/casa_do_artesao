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
    calcular_metricas_territoriais,
    calcular_metricas_temporais,
)
from services.normalize import normalizar_dados
from services.validator import validar_consistencia

st.set_page_config(page_title="Casa do Artesão", layout="wide")

st.title("Dashboard Casa do Artesão")

df = carregar_dados()
df = limpar_dados(df)
df = normalizar_dados(df)
df = criar_colunas_derivadas(df)


# ERROS
erros = validar_consistencia(df)

if erros:
    st.warning("Inconsistências encontradas")

    for erro in erros:
        st.write(erro)

else:
    st.sucess("Nenhuma inconsistência encontrada")


if df.empty:
    st.error("Dataset vazio")

st.header("Indicadores Gerais")
# CRIA CARDS
# CALCULAR METRICAS
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


# CALCULAR METRICAS DEMOGRAFICAS
st.header("Perfil Demográfico")

metricas_demo = calcular_metricas_demograficas(df)

metricas_demo["genero"].columns = ["genero", "quantidade"]

fig_genero = px.pie(
    metricas_demo["genero"],
    names="genero",
    values="quantidade",
    hole=0.5,
    title="Distribuição por Gênero",
)


metricas_demo["raca"].columns = ["raca", "quantidade"]

fig_raca = px.bar(
    metricas_demo["raca"],
    x="quantidade",
    y="raca",
    orientation="h",
    title="Distribuição por Raça",
)


metricas_demo["faixa_etaria"].columns = ["faixa_etaria", "quantidade"]

fig_faixa = px.bar(
    metricas_demo["faixa_etaria"],
    x="faixa_etaria",
    y="quantidade",
    title="Distribuição por Faixa Etária",
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


# CALCULAR METRICAS ECONOMICAS
st.header("Perfil Econômico")
metricas_economicas = calcular_metricas_economicas(df)

metricas_economicas["renda_artesanato"].columns = ["percentual", "quantidade"]

fig_renda = px.bar(
    metricas_economicas["renda_artesanato"],
    x="percentual",
    y="quantidade",
    title="Fonte de Renda Principal",
)


metricas_economicas["outra_renda"].columns = ["outra_renda", "quantidade"]

fig_outra_renda = px.pie(
    metricas_economicas["outra_renda"],
    names="outra_renda",
    values="quantidade",
    hole=0.5,
    title="Outra Fonte de Renda",
)

metricas_economicas["aposentado"].columns = ["aposentado", "quantidade"]

fig_aposentado = px.pie(
    metricas_economicas["aposentado"],
    names="aposentado",
    values="quantidade",
    hole=0.5,
    title="Aposentados",
)


metricas_economicas["pensionista"].columns = ["pensionista", "quantidade"]

fig_pensionista = px.pie(
    metricas_economicas["pensionista"],
    names="pensionista",
    values="quantidade",
    hole=0.5,
    title="Pensionistas",
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

# METRICAS TERRITORIAIS
st.header("Metricas Territoriais")
metricas_territoriais = calcular_metricas_territoriais(df)

metricas_territoriais["feira"].columns = ["feira", "quantidade"]

fig_feira = px.bar(
    metricas_territoriais["feira"],
    x="quantidade",
    y="feira",
    orientation="h",
    title="Artesãos por Feira",
)


fig_genero_feira = px.bar(
    metricas_territoriais["genero_por_feira"],
    x="feira",
    y="quantidade",
    color="genero",
    barmode="group",
    title="Distribuição de Gênero por Feira",
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_feira, use_container_width=True)
with col2:
    st.plotly_chart(fig_genero_feira, use_container_width=True)

# METRICAS ATUAÇÂO
st.header("Atuação dos Artesãos")
metricas_atuacao = calcular_metricas_atuacao(df)

metricas_atuacao["tecnicas"].columns = ["tecnica", "quantidade"]

fig_tecnicas = px.bar(
    metricas_atuacao["tecnicas"],
    x="quantidade",
    y="tecnica",
    orientation="h",
    title="Técnicas Mais Utilizadas",
)

metricas_atuacao["produtos"].columns = ["produto", "quantidade"]

fig_produtos = px.bar(
    metricas_atuacao["produtos"],
    x="quantidade",
    y="produto",
    orientation="h",
    title="Produtos Mais Produzidos",
)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig_tecnicas, use_container_width=True)
with col4:
    st.plotly_chart(fig_produtos, use_container_width=True)


st.header("Formalização (MEI)")

metricas_formalizacao = calcular_metricas_formalizacao(df)

fig_mei = px.bar(
    metricas_formalizacao["mei_por_feira"],
    x="feira",
    y="quantidade",
    color="mei",
    barmode="group",
    title="MEI por Feira",
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Percentual Geral de MEI", f"{metricas_formalizacao['percentual_mei']:.1f}%"
    )
with col2:
    st.metric("Feira com Mais MEIs", metricas_formalizacao["feira_mais_mei"])

st.plotly_chart(fig_mei, use_container_width=True)


st.header("Evolução Temporal")

metricas_temporais = calcular_metricas_temporais(df)

fig_temporal = px.line(
    metricas_temporais["cadastro_por_mes"],
    x="mes",
    y="quantidade",
    markers=True,
    title="Evolução de Cadastros"
)

st.plotly_chart(fig_temporal, use_container_width=True)

# SIDEBAR
st.sidebar.title("Casa do Artesão")

st.sidebar.markdown("---")

filtro_feira = st.sidebar.multiselect(
    "Filtrar por feira", options=df["feira"].unique(), default=df["feira"].unique()
)

filtro_genero = st.sidebar.multiselect(
    "Filtro por gênero", options=df["genero"].unique(), default=df["genero"].unique()
)

df_filtrado = df[(df["feira"].isin(filtro_feira)) & (df["genero"].isin(filtro_genero))]
