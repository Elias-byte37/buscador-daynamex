import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Buscador Daynamex", layout="centered")

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNPiCLWRdXv7mE3SSoIxh055sOftk2JzVOxrNBulDzbzqooFV2erznw-9HpyEIBhtASghBxZcFTSvX/pub?gid=68779616&single=true&output=csv"

@st.cache_data(ttl=600)
def get_data():
    r = requests.get(URL)
    return pd.read_csv(io.StringIO(r.text))

try:
    df = get_data()
    df.columns = df.columns.str.strip() # Limpia espacios en nombres de columnas
    
    st.title("🔍 Buscador Daynamex 2026")
    busqueda = st.text_input("Ingresa modelo, marca o motor:")
    
    if busqueda:
        # Busca en toda la fila convirtiendo todo a texto
        mask = df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)
        res = df[mask]
        
        if not res.empty:
            for _, row in res.iterrows():
                st.divider()
                # Esto mostrará TODA la información disponible en esa fila, sin fallar
                st.write(row.to_frame().transpose().reset_index(drop=True))
        else:
            st.warning("No se encontraron resultados.")
except Exception as e:
    st.error(f"Error cargando datos: {e}")
