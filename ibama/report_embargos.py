import streamlit as st
import pandas as pd
import plotly.express as px
import ast

# Título da aplicação
st.set_page_config(page_title="Dashboard de Embargos", layout="wide")
st.title("📊 Dashboard de Embargos Ambientais - IBAMA")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    #url = "https://lcsbkt.s3.us-east-2.amazonaws.com/gold/relatorio_estatistico_embargos.csv"
    df = pd.read_csv('relatorio_estatistico_embargos.csv')
    return df

# Função para transformar string-dict em DataFrame
def parse_dict_column(column, key_name="Chave"):
    parsed_dict = ast.literal_eval(column)
    return pd.DataFrame(parsed_dict.items(), columns=[key_name, "Registros"])

# Carrega os dados
df = carregar_dados()

# Exibir dados brutos
with st.expander("🔍 Ver dados brutos"):
    st.dataframe(df)

# Gráfico de registros por estado
st.subheader("📍 Registros por Estado")
estados_df = parse_dict_column(df.loc[0, "Estados"], key_name="Estado")
estados_df = estados_df.sort_values(by="Registros", ascending=False)
fig_estado = px.bar(estados_df.head(20), x="Estado", y="Registros", color="Registros", text="Registros")
st.plotly_chart(fig_estado, use_container_width=True)

# Gráfico de registros por município
st.subheader("🏙️ Registros por Município")
municipios_df = parse_dict_column(df.loc[0, "Municípios"], key_name="Município")
municipios_df = municipios_df.sort_values(by="Registros", ascending=False)
fig_municipio = px.bar(municipios_df.head(20), x="Município", y="Registros", color="Registros", text="Registros")
st.plotly_chart(fig_municipio, use_container_width=True)

# Área total desmatada
st.subheader("🌱 Área Total Desmatada")
area_total = df["Área Total Desmatada"].iloc[0]
st.metric("Área Total Desmatada (ha)", f"{float(area_total):,.2f}")

# Gráfico por ano da infração
st.subheader("📅 Infrações por Ano")
anos_col = df["Ano da Infração"].dropna()
if not anos_col.empty and isinstance(anos_col.iloc[0], str):
    anos_dict = ast.literal_eval(anos_col.iloc[0])
    anos_df = pd.DataFrame(anos_dict.items(), columns=["Ano", "Registros"])
    anos_df = anos_df.sort_values(by="Ano")
    fig_ano = px.line(anos_df, x="Ano", y="Registros", markers=True)
    st.plotly_chart(fig_ano, use_container_width=True)
else:
    st.info("Não há dados disponíveis de anos.")

# Gráfico de artigos da legislação (se disponível)
if "Artigos da Legislação" in df.columns:
    artigos_raw = df["Artigos da Legislação"].dropna()
    if not artigos_raw.empty and isinstance(artigos_raw.iloc[0], str):
        try:
            artigos_dict = ast.literal_eval(artigos_raw.iloc[0])
            artigos_df = pd.DataFrame(artigos_dict.items(), columns=["Artigo", "Registros"])
            artigos_df = artigos_df.sort_values(by="Registros", ascending=False)
            st.subheader("📚 Artigos da Legislação Mais Citados")
            fig_artigos = px.bar(artigos_df.head(10), x="Artigo", y="Registros", text="Registros", color="Registros")
            st.plotly_chart(fig_artigos, use_container_width=True)
        except Exception:
            st.warning("Não foi possível processar os dados de artigos da legislação.")

# Rodapé
st.caption("🔗 Fonte: IBAMA • Dados públicos hospedados em AWS S3")
