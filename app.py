import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely import wkt
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# Título
st.title("Análise de Dados Geoespaciais - Uso e Cobertura")

# Upload do arquivo
uploaded_file = st.file_uploader("Carregue seu arquivo CSV", type=["csv"])

if uploaded_file is not None:
    # Leitura dos dados
    df = pd.read_csv(uploaded_file)
    
    # Converter geometria de WKT para objeto geométrico
    df['geometry'] = df['geom'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

    # Estatísticas gerais
    st.subheader("📊 Estatísticas Descritivas")
    st.write(df.describe(include='all'))

    # Gráficos
    st.subheader("📈 Gráficos de Distribuição")

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Distribuição por Estado")
        st.bar_chart(df['state'].value_counts())
    
    with col2:
        st.write("Distribuição por Classe")
        st.bar_chart(df['main_class'].value_counts())

    st.write("Distribuição da Área (km²)")
    fig, ax = plt.subplots()
    df['area_km'].hist(bins=30, ax=ax)
    ax.set_xlabel("Área (km²)")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

    # Mapa interativo
    st.subheader("🗺️ Mapa Interativo")

    m = folium.Map(location=[-3, -60], zoom_start=4, tiles='CartoDB positron')

    for _, row in gdf.iterrows():
        folium.GeoJson(
            row['geometry'],
            tooltip=f"Classe: {row['main_class']}<br>Área: {row['area_km']} km²<br>Data: {row['image_date']}"
        ).add_to(m)

    st_folium(m, width=700, height=500)
