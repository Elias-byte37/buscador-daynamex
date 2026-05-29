import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Buscador Daynamex", layout="centered")

# URL de tu CSV publicado
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNPiCLWRdXv7mE3SSoIxh055sOftk2JzVOxrNBulDzbzqooFV2erznw-9HpyEIBhtASghBxZcFTSvX/pub?gid=68779616&single=true&output=csv"

@st.cache_data(ttl=600)
def get_data():
    try:
        r = requests.get(URL)
        r.raise_for_status() 
        return pd.read_csv(io.StringIO(r.text))
    except Exception as e:
        st.error(f"Error al descargar los datos: {e}")
        return pd.DataFrame()

try:
    df = get_data()
    if not df.empty:
        # Limpiamos espacios en nombres de columnas
        df.columns = df.columns.str.strip()
        
        st.title("🔍 Buscador Comercial Daynamex")
        st.markdown("---")
        busqueda = st.text_input("Ingresa el modelo, marca o nombre del auto:")
        
        if busqueda:
            # La magia: esta línea busca en TODAS las columnas a la vez
            mask = df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)
            res = df[mask]
            
            if not res.empty:
                st.success(f"Se encontraron {len(res)} resultados:")
                for _, row in res.iterrows():
                    with st.container(border=True):
                        # Buscamos dinámicamente la columna que contenga "imagen"
                        col_imagen = next((c for c in df.columns if 'imagen' in c.lower()), None)
                        
                        if col_imagen and pd.notna(row[col_imagen]):
                            img_link = str(row[col_imagen]).strip()
                            # Corrector automático para links de imgbb
                            if "ibb.co" in img_link and not img_link.endswith((".jpg", ".png", ".jpeg")):
                                img_link = img_link.replace("ibb.co", "i.ibb.co") + ".jpg"
                            if not img_link.startswith("http"):
                                img_link = "https://" + img_link
                                
                            try:
                                st.image(img_link, width=300)
                            except:
                                st.warning("No se pudo cargar la imagen.")
                        
                        # Mostramos TODAS las columnas dinámicamente
                        for col in df.columns:
                            # Ignoramos la columna de imagen para no repetirla y mostramos el resto
                            if col != col_imagen and pd.notna(row[col]):
                                st.write(f"**{col}:** {row[col]}")
            else:
                st.warning("No se encontraron resultados.")
        else:
            st.info("Escribe algo arriba para comenzar a buscar.")
    else:
        st.error("La hoja de cálculo está vacía o hubo un error al cargar.")
except Exception as e:
    st.error(f"Error general: {e}")
```eof

### ¿Qué pasos debes seguir?
1. **Actualiza tu Google Sheets:** Asegúrate de que las columnas nuevas tengan los nombres claros.
2. **Commit:** Pega este código en `app.py` y dale a "Commit changes".
3. **Reboot:** En Streamlit, dale a "Reboot app" para que tome los nuevos nombres de columnas.

¡Ahora, cada vez que agregues un nuevo campo en tu Excel, aparecerá automáticamente en el buscador sin que tengas que tocar el código nunca más!
