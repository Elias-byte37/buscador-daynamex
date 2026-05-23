import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Buscador Daynamex", layout="centered")

# URL de tu CSV publicado
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
    busqueda = st.text_input("Ingrese el modelo del convertidor:")
    
    if busqueda:
        # Filtro de búsqueda
        mask = df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)
        res = df[mask]
        
        if not res.empty:
            st.success(f"Se encontraron {len(res)} resultados:")
            for _, row in res.iterrows():
                with st.container(border=True):
                    # Buscamos la columna de imagen
                    col_imagen = next((c for c in df.columns if c.lower() == 'imagen'), None)
                    
                    if col_imagen and pd.notna(row[col_imagen]):
                        img_link = str(row[col_imagen]).strip()
                        
                        # Asegurar que el link sea HTTPS completo
                        if not img_link.startswith("http"):
                            img_link = "https://" + img_link
                            
                        # Intentar mostrar la imagen
                        try:
                            st.image(img_link, width=300, caption="Foto del Producto")
                        except:
                            st.error("No se pudo cargar la imagen. Verifica que el link en Google Sheets sea público y directo.")
                    
                    # Mostrar datos de forma limpia (excluyendo la columna Imagen)
                    for col in df.columns:
                        if col.lower() != 'imagen' and pd.notna(row[col]):
                            st.write(f"**{col}:** {row[col]}")
        else:
            st.warning("No se encontraron resultados.")
    else:
        st.info("Escribe algo arriba para comenzar a buscar.")
except Exception as e:
    st.error(f"Error al cargar la aplicación: {e}")
