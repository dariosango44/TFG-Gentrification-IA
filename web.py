#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 17:04:32 2025

@author: dariosango44
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# 2. CARGAR DATOS (Usamos caché para que no cargue lento cada vez que tocas un botón)
@st.cache_data
def cargar_datos():
    # Asegúrate de que el nombre del archivo coincide con el tuyo
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
    # Filtramos los datos por el barrio seleccionado
    datos_barrio = df[df['Territori'] == barrio_seleccionado].iloc[0]
    
    precio_2015 = datos_barrio['2015']
    precio_2023 = datos_barrio['2023']
    crecimiento = datos_barrio['Crecimiento_%']
    
    # Mostramos métricas grandes
    col1, col2, col3 = st.columns(3)
    col1.metric("Precio 2015", f"{precio_2015} €/m²")
    col2.metric("Precio 2023", f"{precio_2023} €/m²")
    col3.metric("Crecimiento", f"{crecimiento:.2f}%", delta_color="inverse")

    # 5. GRÁFICO DE EVOLUCIÓN TEMPORAL
    st.subheader(f"Evolución del precio en {barrio_seleccionado}")
    
    # Preparamos los datos para el gráfico (Años vs Precio)
    # Cogemos solo las columnas que son años (desde la columna 2 hasta la antepenúltima)
    # Ajusta esto según tus columnas, normalmente los años son columnas numéricas
    columnas_anos = [col for col in df.columns if col.isnumeric()]
    
    valores = datos_barrio[columnas_anos]
    
    # Creamos el gráfico de líneas
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(columnas_anos, valores, marker='o', color='royalblue')
    ax.set_title("Evolución Histórica (2000-2023)")
    ax.set_ylabel("Precio (€/m²)")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Mostrar gráfico en Streamlit
    st.pyplot(fig)

    # 6. TABLA DE DATOS (Solo del barrio)
    with st.expander("Ver datos brutos de este barrio"):
        st.dataframe(datos_barrio)

except FileNotFoundError:
    st.error("No encuentro el archivo 'datos_con_metricas.csv'. Ejecuta primero el script de análisis.")
except Exception as e:
    st.error(f"Ocurrió un error: {e}")