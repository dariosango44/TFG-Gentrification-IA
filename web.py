import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # <--- FALTABA ESTO: Para cálculos numéricos
from sklearn.linear_model import LinearRegression # <--- FALTABA ESTO: Para la IA predictiva

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Gentrification Radar AI",
    page_icon="🏠",
    layout="wide"
)

# Título y descripción
st.title("🏠 Gentrification Radar AI")
st.markdown("""
Esta aplicación analiza la evolución del precio del alquiler en **Barcelona** 
para detectar zonas tensionadas y gentrificación usando datos históricos.
""")

# 2. CARGAR DATOS
@st.cache_data
def cargar_datos():
    # Asegúrate de que el nombre del archivo es correcto
    df = pd.read_csv('datos_con_metricas.csv', sep=';')
    return df

try:
    df = cargar_datos()
    
    # 3. BARRA LATERAL (FILTROS)
    st.sidebar.header("🔍 Filtros")
    
    # Selector de barrio
    lista_barrios = df['Territori'].unique().tolist()
    barrio_seleccionado = st.sidebar.selectbox("Selecciona un Barrio", lista_barrios)
    
    # 4. KPI's (INDICADORES CLAVE)
    datos_barrio = df[df['Territori'] == barrio_seleccionado].iloc[0]
    
    precio_2015 = datos_barrio['2015']
    precio_2023 = datos_barrio['2023']
    crecimiento = datos_barrio['Crecimiento_%']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Precio 2015", f"{precio_2015} €/m²")
    col2.metric("Precio 2023", f"{precio_2023} €/m²")
    col3.metric("Crecimiento", f"{crecimiento:.2f}%", delta_color="inverse")

    # 5. GRÁFICO 1: EVOLUCIÓN HISTÓRICA (El pasado)
    st.subheader(f"Evolución histórica en {barrio_seleccionado}")
    columnas_anos = [col for col in df.columns if col.isnumeric()]
    valores = datos_barrio[columnas_anos]
    
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(columnas_anos, valores, marker='o', color='royalblue')
    ax1.set_title("Evolución (2000-2023)")
    ax1.set_ylabel("Precio (€/m²)")
    ax1.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig1)

    # 6. GRÁFICO 2: PREDICCIÓN (El futuro - Machine Learning)
    st.markdown("---")
    st.subheader(f"🤖 Predicción IA: Futuro de {barrio_seleccionado}")

    # Preparamos datos para el modelo
    X = np.array([int(anio) for anio in columnas_anos]).reshape(-1, 1)
    y = datos_barrio[columnas_anos].values

    # Entrenamos el modelo
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Predecimos 2024, 2025, 2026
    anos_futuros = np.array([2024, 2025, 2026]).reshape(-1, 1)
    prediccion = modelo.predict(anos_futuros)

    # Gráfico con predicción
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(X, y, marker='o', color='royalblue', label='Datos Reales')
    
    # Unimos gráficamente el último dato real con la predicción
    X_futuro_completo = np.concatenate((X[[-1]], anos_futuros))
    y_futuro_completo = np.concatenate((y[[-1]], prediccion))
    
    ax2.plot(X_futuro_completo, y_futuro_completo, linestyle='--', marker='x', color='salmon', label='Predicción IA')
    ax2.set_title(f"Proyección a 3 años")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

    # Texto explicativo de la predicción
    tendencia = "subida" if prediccion[-1] > y[-1] else "bajada"
    st.info(f"El algoritmo de Regresión Lineal estima una **{tendencia}** constante. Precio esperado en 2025: **{prediccion[1]:.2f} €/m²**.")

    # 7. TABLA DE DATOS
    with st.expander("Ver datos brutos"):
        st.dataframe(datos_barrio)

    # 8. CHATBOT (Interfaz)
    st.markdown("---")
    st.subheader("Asistente de Vivienda (IA)")

    # Historial del chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Pintar mensajes antiguos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    if prompt := st.chat_input("Pregunta algo (ej: ¿Cuál es el barrio más caro?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Respuesta Dummy (Aquí conectaremos una IA pronto)
        respuesta = f"He recibido tu pregunta: '{prompt}'. Mi cerebro aún se está conectando, pero pronto podré analizar los datos por ti."
        
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

except FileNotFoundError:
    st.error("No encuentro el archivo 'datos_con_metricas.csv'. Ejecuta primero 'analisis_gentrificacion.py'.")
except Exception as e:
    st.error(f"Error inesperado: {e}")