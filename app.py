import streamlit as st
import pandas as pd
import requests
import io

# Configuración de la página
st.set_page_config(page_title="Buscador Daynamex", layout="centered")

# URL de tu base de datos en Google Sheets
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNPiCLWRdXv7mE3SSoIxh055sOftk2JzVOxrNBulDzbzqooFV2erznw-9HpyEIBhtASghBxZcFTSvX/pub?gid=68779616&single=true&output=csv"

# Carga de datos
@st.cache_data(ttl=600)
def get_data():
    r = requests.get(URL)
    return pd.read_csv(io.StringIO(r.text))

try:
    df = get_data()
    df.columns = df.columns.str.strip()
    
    st.title("🔍 Buscador Daynamex 2026")
    busqueda = st.text_input("Ingresa modelo, marca o motor:")
    
    if busqueda:
        mask = df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)
        res = df[mask]
        
        if not res.empty:
            for _, row in res.iterrows():
                st.divider()
                st.subheader(f"{row.get('Marca', '')} {row.get('Submarca', '')}")
                st.write(f"**Producto:** {row.get('Nombre del articulo', '')}")
                st.info(f"**Precio:** ${row.get('Precio', '')}")
        else:
            st.warning("No se encontraron resultados.")
except Exception:
    st.error("Error al cargar los datos.")
