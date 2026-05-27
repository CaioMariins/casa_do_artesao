import streamlit as st
from services.cleaning import limpar_dados
from services.features import criar_colunas_derivadas
from services.loader import carregar_dados
from services.metrics import (
    calclular_metricas,
    calcular_metricas_atuacao,
    calcular_metricas_demograficas,
    calcular_metricas_economicas,
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

col1, col2, col3 = st.columns(3)

with col1:
    st.write("### Gênero")
    st.dataframe(metricas_demo["genero"])

with col2:
    st.write("### Raça")
    st.dataframe(metricas_demo["raca"])

with col3:
    st.write("### Faixa Etária")
    st.dataframe(metricas_demo["faixa_etaria"])


st.write("### Pessoas com Deficiência")

col1, col2 = st.columns(2)

with col1:
    st.metric("PCD", metricas_demo["pcd"].get("Sim", 0))

with col2:
    st.metric("Não PCD", metricas_demo["pcd"].get("Não", 0))


# CALCULAR METRICAS ECONOMICAS
st.header("Perfil Econômico")
metricas_economicas = calcular_metricas_economicas(df)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fonte de Renda Principal")
    st.dataframe(metricas_economicas["renda_artesanato"])

with col2:
    st.subheader("Outra fonte de renda")
    st.dataframe(metricas_economicas["outra_renda"])

col3, col4 = st.columns(2)

with col3:
    st.subheader("Aposentados")
    st.dataframe(metricas_economicas["aposentado"])

with col4:
    st.subheader("Pensionistas")
    st.dataframe(metricas_economicas["pensionista"])


# CALCULAR METRICAS ATUAÇÂO
st.header("Atuação dos Artesãos")
metricas_atuacao = calcular_metricas_atuacao(df)

st.subheader("Métricas de Atuação")

col1, col2 = st.columns(2)

with col1:
    st.write("### Artesãos por Feira")
    st.dataframe(metricas_atuacao["feiras"])

with col2:
    st.write("### Técnicas Mais Utilizadas")
    st.dataframe(metricas_atuacao["tecnicas"])

col3, col4 = st.columns(2)

with col3:
    st.write("### Produtos Mais Utilizados")
    st.dataframe(metricas_atuacao["produtos"])

with col4:
    st.write("### CNAEs Mais Frequentes")
    st.dataframe(metricas_atuacao["cnaes"])

# SIDEBAR
st.sidebar.title("Casa do Artesão")

st.sidebar.markdown("---")

filtro_feira = st.sidebar.multiselect(
    "Filtrar por feira",
    options=df["feira"].unique(),
    default=df["feira"].unique()
)

filtro_genero = st.sidebar.multiselect(
    "Filtro por gênero",
    options=df["genero"].unique(),
    default=df["genero"].unique()
)

df_filtrado = df[
    (df["feira"].isin(filtro_feira)) &
    (df["genero"].isin(filtro_genero))
]