import streamlit as st
import pandas as pd
import requests
import io

# Configuración inicial
st.set_page_config(page_title="Buscador Daynamex", layout="centered")

# Estilos CSS para el diseño Daynamex (Oscuro con toques naranjas)
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #333; color: white; border: 1px solid #ff9900; }
    div[data-testid="stExpander"] { background-color: #262626; border: 1px solid #ff9900; }
    h1 { color: #ff9900; text-align: center; font-weight: bold; }
    .stSuccess { background-color: #332d1a; color: #ff9900; }
    </style>
    """, unsafe_allow_html=True)

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNPiCLWRdXv7mE3SSoIxh055sOftk2JzVOxrNBulDzbzqooFV2erznw-9HpyEIBhtASghBxZcFTSvX/pub?gid=68779616&single=true&output=csv"

@st.cache_data(ttl=600)
def get_data():
    r = requests.get(URL)
    return pd.read_csv(io.StringIO(r.text))

try:
    df = get_data()
    df.columns = df.columns.str.strip()
    
    st.title("🔍 DAYNAMEX 2026")
    busqueda = st.text_input("Buscar modelo, marca o motor:")
    
    if busqueda:
        mask = df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)
        res = df[mask]
        
        if not res.empty:
            for _, row in res.iterrows():
                with st.expander(f"⚙️ {row.get('Submarca', 'Producto')}"):
                    if 'Imagen' in row and pd.notna(row['Imagen']):
                        st.image(row['Imagen'], use_container_width=True)
                    st.write(f"**Nombre:** {row.get('Nombre del articulo', 'N/A')}")
                    st.write(f"**Motor:** {row.get('Motor', 'N/A')}")
                    st.markdown(f"<h3 style='color: #ff9900;'>Precio: ${row.get('Precio', '0')}</h3>", unsafe_allow_html=True)
        else:
            st.warning("No se encontraron resultados.")
except Exception:
    st.error("Error al cargar los datos.")
