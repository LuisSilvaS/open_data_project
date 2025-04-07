import pandas as pd
import folium
import re
import streamlit as st
from streamlit_folium import st_folium

# Função para extrair coordenadas
def extrair_coords(geom):
    match = re.search(r'POINT\s*\(([-\d\.]+)\s+([-\d\.]+)\)', str(geom))
    if match:
        return float(match.group(2)), float(match.group(1))  # latitude, longitude
    return None, None

# Streamlit App
st.title("Visualização de Infrações Ambientais")

# Campo para digitar ou selecionar a URL pública do CSV
default_url = "https://lcsbkt.s3.us-east-2.amazonaws.com/bronze/vw_brasil_adm_auto_infracao_p.csv"  # substitua aqui
csv_url = st.text_input("Insira a URL pública do CSV", value=default_url)

if csv_url:
    try:
        df = pd.read_csv(csv_url)

        # Extrair coordenadas
        df[['latitude', 'longitude']] = df['geom'].apply(lambda x: pd.Series(extrair_coords(x)))
        df_coords = df.dropna(subset=['latitude', 'longitude'])

        # Indicadores
        st.subheader("Indicadores")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Infrações", len(df_coords))
        col2.metric("Municípios únicos", df_coords['municipio'].nunique())
        col3.metric("Estados únicos", df_coords['uf'].nunique())

        # Criar o mapa
        mapa = folium.Map(location=[df_coords['latitude'].mean(), df_coords['longitude'].mean()], zoom_start=5)

        for _, row in df_coords.iterrows():
            popup_text = f"""
            <strong>Infrator:</strong> {row.get('nome_infrator', '')}<br>
            <strong>Infração:</strong> {row.get('des_infracao', '')}<br>
            <strong>Data:</strong> {row.get('dat_hora_auto_infracao', '')}<br>
            <strong>Município:</strong> {row.get('municipio', '')} - {row.get('uf', '')}
            """
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color="red", icon="exclamation-sign")
            ).add_to(mapa)

        st.subheader("Mapa de Infrações")
        st_data = st_folium(mapa, width=700, height=500)

    except Exception as e:
        st.error(f"Erro ao carregar o CSV: {e}")
else:
    st.info("Informe uma URL pública de um arquivo CSV contendo a coluna 'geom' com o formato POINT(lon lat).")
