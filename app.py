import streamlit as st
import pandas as pd
from streamlit_extras.copy_to_clipboard import copy_to_clipboard

# Configuración de página
st.set_page_config(page_title="Daynamex | Ventas", layout="centered")

# --- CARGA DE DATOS ---
URL_DE_TU_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNPiCLWRdXv7mE3SSoIxh055sOftk2JzVOxrNBulDzbzqooFV2erznw-9HpyEIBhtASghBxZcFTSvX/pub?gid=68779616&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_csv(URL_DE_TU_CSV)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error al cargar la base de datos: {e}")
        return pd.DataFrame()

df = load_data()

# --- INTERFAZ ---
st.title("🔍 Daynamex Ventas 2026")
st.markdown("Buscador oficial para el equipo de ventas.")

busqueda = st.text_input("Escribe modelo, marca o motor...", placeholder="Ej: Jetta 2015")

if busqueda and not df.empty:
    mask = df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)
    resultados = df[mask]
    
    if not resultados.empty:
        st.write(f"Se encontraron {len(resultados)} resultados:")
        for idx, row in resultados.iterrows():
            with st.container(border=True):
                st.subheader(f"{row.get('Marca', '')} {row.get('Submarca', '')}")
                st.caption(f"Motor: {row.get('Motor', '')} | Año: {row.get('Año', '')}")
                st.success(f"**Producto:** {row.get('Nombre del articulo', '')}")
                st.info(f"**Precio:** ${row.get('Precio', '')} | **Posición:** {row.get('Posicion', '')}")
                
                texto = (f"¡Hola! Confirmamos la pieza para tu {row.get('Marca', '')} {row.get('Submarca', '')} "
                         f"({row.get('Motor', '')}, {row.get('Año', '')}). El producto es el {row.get('Nombre del articulo', '')} "
                         f"y tiene un precio de ${row.get('Precio', '')}. ¿Te gustaría apartarlo?")
                
                if copy_to_clipboard(texto, label="📋 Copiar cotización para WhatsApp"):
                    st.toast("¡Cotización copiada!", icon="✅")
    else:
        st.warning("No se encontraron resultados.")
else:
    st.info("Escribe algo en el buscador para empezar.")
