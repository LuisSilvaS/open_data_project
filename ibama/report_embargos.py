import streamlit as st
import pandas as pd
import plotly.express as px
import ast

# Título
st.title("📊 Dashboard de Embargos Ambientais")

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    url = "https://lcsbkt.s3.us-east-2.amazonaws.com/gold/relatorio_estatistico_embargos.csv"
    df = pd.read_csv(url)
    return df

df = carregar_dados()

# Mostra dados brutos se o usuário quiser
if st.checkbox("🔍 Mostrar dados brutos"):
    st.dataframe(df)

# Conversão das colunas que estão em formato de string dicionário
def parse_dict_column(column):
    return pd.DataFrame(ast.literal_eval(column).items(), columns=[column.name, "Registros"])

# Estados com mais infrações
st.subheader("📍 Registros por Estado")
estados_df = parse_dict_column(df.loc[0, "Estados"])
estados_df = estados_df.sort_values(by="Registros", ascending=False)
fig_estado = px.bar(estados_df.head(15), x="Estados", y="Registros", color="Registros", text="Registros")
st.plotly_chart(fig_estado, use_container_width=True)

# Municípios com mais infrações
st.subheader("🏙️ Registros por Município")
municipios_df = parse_dict_column(df.loc[0, "Municípios"])
municipios_df = municipios_df.sort_values(by="Registros", ascending=False)
fig_municipio = px.bar(municipios_df.head(15), x="Municípios", y="Registros", color="Registros", text="Registros")
st.plotly_chart(fig_municipio, use_container_width=True)

# Área total desmatada
st.subheader("🌱 Área Total Desmatada")
area = df["Área Total Desmatada"].iloc[0]
st.metric(label="Área Total Desmatada (ha)", value=f"{float(area):,.2f}")

# Ano da Infração
st.subheader("📅 Ano das Infrações")
anos = df["Ano da Infração"].dropna()
if not anos.empty:
    anos_list = eval(anos.iloc[0]) if isinstance(anos.iloc[0], str) else anos.iloc[0]
    anos_df = pd.DataFrame(anos_list.items(), columns=["Ano", "Registros"])
    anos_df = anos_df.sort_values("Ano")
    fig_ano = px.line(anos_df, x="Ano", y="Registros", markers=True)
    st.plotly_chart(fig_ano, use_container_width=True)
else:
    st.info("Sem dados de ano de infração disponíveis.")

# Artigos da Legislação (se aplicável)
if "Artigos da Legislação" in df.columns:
    st.subheader("📚 Artigos Mais Citados")
    artigos = df["Artigos da Legislação"].dropna()
    if not artigos.empty and isinstance(artigos.iloc[0], str):
        artigos_list = ast.literal_eval(artigos.iloc[0])
        artigos_df = pd.DataFrame(artigos_list.items(), columns=["Artigo", "Registros"])
        artigos_df = artigos_df.sort_values("Registros", ascending=False)
        fig_artigos = px.bar(artigos_df.head(10), x="Artigo", y="Registros", text="Registros", color="Registros")
        st.plotly_chart(fig_artigos, use_container_width=True)

# Rodapé
st.caption("Fonte: IBAMA / Dados processados via AWS S3")
