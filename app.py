import streamlit as st
import pandas as pd
import requests
import io

# Configuración básica
st.set_page_config(page_title="Buscador Daynamex", layout="centered")

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNPiCLWRdXv7mE3SSoIxh055sOftk2JzVOxrNBulDzbzqooFV2erznw-9HpyEIBhtASghBxZcFTSvX/pub?gid=68779616&single=true&output=csv"

@st.cache_data(ttl=600)
def get_data():
    r = requests.get(URL)
    return pd.read_csv(io.StringIO(r.text))

try:
    df = get_data()
    df.columns = df.columns.str.strip()
    
    st.title("🔍 Buscador Comercial Daynamex")
    st.markdown("---")
    busqueda = st.text_input("Ingresa modelo, marca o motor para buscar:")
    
    if busqueda:
        mask = df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)
        res = df[mask]
        
        if not res.empty:
            st.success(f"Se encontraron {len(res)} resultados:")
            for _, row in res.iterrows():
                with st.container(border=True):
                    # Mostramos toda la información disponible en la fila
                    st.write(row.to_frame().transpose().reset_index(drop=True))
        else:
            st.warning("No se encontraron resultados para tu búsqueda.")
    else:
        st.info("Escribe algo arriba para comenzar a buscar.")
except Exception as e:
    st.error("Error al cargar los datos. Verifica la conexión.")
