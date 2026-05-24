import streamlit as st
from services.cleaning import limpar_dados
from services.features import criar_colunas_derivadas
from services.loader import carregar_dados
from services.normalize import normalizar_dados
from services.validator import validar_consistencia
from services.metrics import calclular_metricas, calcular_metricas_demograficas

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

st.dataframe(df.head())

# CRIA CARDS

metricas = calclular_metricas(df)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Artesãos", metricas["total_artesaos"])

with col2:
    st.metric("Fixos", metricas["total_fixos"])

with col3:
    st.metric("Visitantes", metricas["total_visitantes"])

with col4:
    st.metric("% MEI", f'{metricas["percentual_mei"]:.1f}%')

metricas_demo = calcular_metricas_demograficas(df)

st.subheader("Métricas Demográficas")

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