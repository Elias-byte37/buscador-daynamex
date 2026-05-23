import streamlit as st
import pandas as pd

# 1. Título y Configuración
st.set_page_config(page_title="Daynamex | Buscador de Convertidores", layout="wide")
st.title("🔍 Buscador Comercial Daynamex 2026")

# 2. Cargar tu Google Sheet (aquí pondrías el link público de tu CSV)
# Sugerencia: Publica tu Google Sheet como CSV y usa ese URL
url = "TU_URL_DE_CSV_AQUI" 
@st.cache_data
def load_data():
    return pd.read_csv(url)

df = load_data()

# 3. Buscador Inteligente
search = st.text_input("¿Qué auto buscas? (Ej: Jetta 2015)")

if search:
    # Filtro sencillo por nombre de auto
    results = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    
    if not results.empty:
        st.write(f"Resultados encontrados: {len(results)}")
        
        for index, row in results.iterrows():
            st.divider()
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"{row['Marca']} {row['Submarca']}")
                st.write(f"**Motor:** {row['Motor']} | **Año:** {row['Año']}")
                st.success(f"**Producto:** {row['Nombre del artículo']} - **Precio:** ${row['Precio']}")
            
            with col2:
                # El botón mágico de copiar
                texto_cotizacion = f"Hola! La pieza para tu {row['Marca']} {row['Submarca']} es el {row['Nombre del artículo']} y tiene un precio de ${row['Precio']}."
                st.button("📋 Copiar cotización", key=index, on_click=lambda t=texto_cotizacion: st.write(f"Copiado al portapapeles: {t}"))
    else:
        st.warning("No se encontró ese modelo. Recuerda revisar si falta cargarlo.")
