import pandas as pd
import streamlit as st

# Título
st.title("Tabla de los tipos de referencia oficiales del mercado hipotecario")

# Cargar archivo Excel con encabezado doble
df = pd.read_excel("archivo_tasas.xlsx", header=[0, 1])

# Unir las columnas multiíndice en una sola cadena
df.columns = ['_'.join([str(a).strip(), str(b).strip()]) for a, b in df.columns]

# Renombrar columnas específicas para facilitar filtros
df = df.rename(columns={"AÑO_AÑO": "AÑO", "MES_MES": "MES"})

# Eliminar filas sin año o mes
df = df.dropna(subset=["AÑO", "MES"])

# Convertir tipos adecuados
df["AÑO"] = df["AÑO"].astype(int)
df["MES"] = df["MES"].astype(str)

# --- FILTROS en sidebar (lado izquierdo) ---
st.sidebar.header("Filtros")

# Opciones para filtros de año y mes
opciones_anio = sorted(df["AÑO"].unique())
opciones_mes = ["Todos"] + sorted(df["MES"].unique())

# Filtro rango año "Desde" y "Hasta"
anio_desde = st.sidebar.selectbox("Año desde", opciones_anio, index=0)
anio_hasta = st.sidebar.selectbox("Año hasta", opciones_anio, index=len(opciones_anio)-1)

# Validar que anio_desde <= anio_hasta
if anio_desde > anio_hasta:
    st.sidebar.error("El 'Año desde' debe ser menor o igual al 'Año hasta'.")

mes_seleccionado = st.sidebar.selectbox("Selecciona el MES", opciones_mes)

valor_buscado = st.sidebar.text_input("Buscar valor específico", "")

# Filtrar el DataFrame según selección
df_filtrado = df.copy()

# Filtro rango años
df_filtrado = df_filtrado[(df_filtrado["AÑO"] >= anio_desde) & (df_filtrado["AÑO"] <= anio_hasta)]

# Filtro mes
if mes_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["MES"] == mes_seleccionado]

# Filtro texto
if valor_buscado:
    df_filtrado = df_filtrado[df_filtrado.apply(
        lambda row: row.astype(str).str.contains(valor_buscado, case=False).any(), axis=1
    )]

# Función para limpiar el número y generar botón PDF
def generar_celda(valor, anio, mes, col_id):
    try:
        if pd.isna(valor):
            return "N/A"
        import re
        match = re.search(r'[\d,.]+', str(valor))
        numero = match.group(0) if match else "N/A"
        enlace_pdf = f"https://tuservidor.com/pdfs/{anio}_{mes}_{col_id}.pdf"
        return (
            f"{numero} &nbsp; "
            f"<a href='{enlace_pdf}' target='_blank' "
            f"style='text-decoration:none;'>"
            f"<button style='font-size:10px;cursor:pointer;'>PDF</button>"
            f"</a>"
        )
    except Exception:
        return "Error"

# Columnas a modificar (excluyendo AÑO y MES)
columnas_a_modificar = [col for col in df_filtrado.columns if col not in ["AÑO", "MES"]]

df_html = df_filtrado.copy()

for col in columnas_a_modificar:
    col_id = col.replace(" ", "_").replace(",", "").replace(".", "")
    df_html[col] = df_html.apply(lambda row: generar_celda(row[col], row["AÑO"], row["MES"], col_id), axis=1)

# Mostrar tabla con HTML no escapado para ver botones y enlaces
st.markdown("<h3>Datos con enlaces PDF</h3>", unsafe_allow_html=True)
st.write("Nota: Asegúrate de que los PDF estén disponibles en el servidor.")

st.markdown(
    df_html.to_html(escape=False, index=False),
    unsafe_allow_html=True
)













































