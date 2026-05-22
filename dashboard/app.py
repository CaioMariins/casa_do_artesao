import streamlit as st
from services.loader import carregar_dados
st.set_page_config(page_title="Casa do Artesão", layout="wide")

st.title("Dashboard Casa do Artesão")

df = carregar_dados()

if df.empty:
    st.error("Dataset vazio")

st.dataframe(df.head())

