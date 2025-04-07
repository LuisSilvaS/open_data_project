# streamlit_app.py
import streamlit as st
import pandas as pd

# URL dos dados
default_url = "https://lcsbkt.s3.us-east-2.amazonaws.com/bronze/vw_brasil_adm_auto_infracao_p.csv"

# Título do app
st.title("Visualizador de Dados - Autos de Infração")

# Carregando os dados
@st.cache_data
def carregar_dados(url):
    return pd.read_csv(url, sep=",", encoding="utf-8")

df = carregar_dados(default_url)

# Mostrar as primeiras linhas
st.subheader("Visualização dos primeiros registros")
st.dataframe(df.head())
