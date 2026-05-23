import streamlit as st
from services.loader import carregar_dados
from services.cleaning import limpar_dados

st.set_page_config(page_title="Casa do Artesão", layout="wide")

st.title("Dashboard Casa do Artesão")

df = carregar_dados()
df = limpar_dados(df)

if df.empty:
    st.error("Dataset vazio")

st.write(f"Total de registros: {len(df)}")
st.dataframe(df.head())
