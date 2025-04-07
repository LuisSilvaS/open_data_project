import streamlit as st
import pandas as pd

default_url = "https://lcsbkt.s3.us-east-2.amazonaws.com/bronze/vw_brasil_adm_auto_infracao_p.csv"

st.title("Visualizador de Autos de Infração - IBAMA")

@st.cache_data
def carregar_dados(url):
    return pd.read_csv(url, sep=",", encoding="utf-8", nrows=500, low_memory=False)

try:
    df = carregar_dados(default_url)
    st.subheader("Visualização dos primeiros registros")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
