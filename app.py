import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Buscador Daynamex", layout="centered")

# --- Logo actualizado ---
LOGO_URL = "https://i.ibb.co/svYK2B05/LOGO-DAYNAMEX.png" 

try:
    st.image(LOGO_URL, width=250)
except:
    st.title("🔍 Buscador Comercial Daynamex")

# --- URLs ---
URL_1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNPiCLWRdXv7mE3SSoIxh055sOftk2JzVOxrNBulDzbzqooFV2erznw-9HpyEIBhtASghBxZcFTSvX/pub?gid=68779616&single=true&output=csv"
URL_2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNPiCLWRdXv7mE3SSoIxh055sOftk2JzVOxrNBulDzbzqooFV2erznw-9HpyEIBhtASghBxZcFTSvX/pub?gid=707680383&single=true&output=csv"

@st.cache_data(ttl=60)
def get_data(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return pd.read_csv(io.StringIO(r.text))
    except Exception as e:
        return pd.DataFrame()

try:
    df1 = get_data(URL_1)
    df2 = get_data(URL_2)
    
    df = pd.concat([df1, df2], ignore_index=True)
    df.columns = df.columns.str.strip()

    if not df.empty:
        st.subheader("Sistema de Inventario")
        st.markdown("---")
        
        busqueda = st.text_input("Ingresa el modelo, marca o nombre del auto:")
        
        if busqueda:
            mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
            res = df[mask]
            
            if not res.empty:
                st.success(f"Se encontraron {len(res)} resultados:")
                for _, row in res.iterrows():
                    with st.container(border=True):
                        col_imagen = next((c for c in df.columns if 'IMAGEN' in c.upper()), None)
                        
                        if col_imagen and pd.notna(row[col_imagen]):
                            img_link = str(row[col_imagen]).strip()
                            if not img_link.startswith("http"):
                                img_link = "https://" + img_link
                            try:
                                st.image(img_link, width=300)
                            except:
                                st.warning("No se pudo cargar la imagen.")
                        
                        for col in df.columns:
                            if col != col_imagen and pd.notna(row[col]):
                                st.write(f"**{col}:** {row[col]}")
            else:
                st.warning("No se encontraron resultados.")
    else:
        st.error("No se detectaron datos.")
except Exception as e:
    st.error(f"Error técnico: {e}")
