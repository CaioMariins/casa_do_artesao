import streamlit as st
from services.cleaning import limpar_dados
from services.features import criar_colunas_derivadas
from services.loader import carregar_dados
from services.normalize import normalizar_dados
from services.validator import validar_consistencia
from services.metrics import calclular_metricas

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