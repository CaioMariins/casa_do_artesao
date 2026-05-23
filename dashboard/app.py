import streamlit as st
from services.cleaning import limpar_dados
from services.features import criar_colunas_derivadas
from services.loader import carregar_dados
from services.normalize import normalizar_dados
from services.validator import validar_consistencia

st.set_page_config(page_title="Casa do Artesão", layout="wide")

st.title("Dashboard Casa do Artesão")

df = carregar_dados()
df = limpar_dados(df)
df = normalizar_dados(df)
df = criar_colunas_derivadas(df)


if df.empty:
    st.error("Dataset vazio")

st.write(f"Total de registros: {len(df)}")
st.dataframe(df.head())

erros = validar_consistencia(df)

if erros:
    st.warning("Inconsistências encontradas")

    for erro in erros:
        st.write(erro)

else:
    st.sucess("Nenhuma inconsistência encontrada")
