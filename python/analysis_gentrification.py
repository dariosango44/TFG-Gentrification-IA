#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 16:58:55 2025

@author: dariosango44
"""

import pandas as pd
import matplotlib.pyplot as plt # Librería para hacer gráficos

# Configuración para que los gráficos se vean bien
plt.style.use('ggplot')

# 1. Cargar tus datos limpios (asegúrate de poner el separador correcto)
df = pd.read_csv('datos_limpios_final.csv', sep=';')

# 2. DEFINIR LA FÓRMULA DE GENTRIFICACIÓN
# Vamos a comparar el año 2015 (inicio recuperación crisis) con el 2023 (actualidad aprox)
# Asegúrate de que esas columnas existen en tu CSV. Si no, cambia los años.
anio_inicio = '2015'
anio_fin = '2023'

print(f"--- Analizando el boom del alquiler entre {anio_inicio} y {anio_fin} ---")

# Creamos una nueva columna calculada: 'Crecimiento_Porcentual'
# Fórmula: ((Valor Final - Valor Inicial) / Valor Inicial) * 100
df['Crecimiento_%'] = ((df[anio_fin] - df[anio_inicio]) / df[anio_inicio]) * 100

# 3. RANKING DE BARRIOS (Top 10 subidas)
# Filtramos para quitar filas que no sean barrios (quitamos Distritos y Ciudad entera si las hay)
# Suponemos que la columna se llama 'Tipus de territori'. Si no, ajusta el nombre.
df_barrios = df[df['Tipus de territori'] == 'Barri'].copy()

# Ordenamos de mayor a menor subida
df_top = df_barrios.sort_values(by='Crecimiento_%', ascending=False).head(10)

print("\nTOP 10 BARRIOS QUE MÁS SE HAN ENCARECIDO:")
print(df_top[['Territori', anio_inicio, anio_fin, 'Crecimiento_%']])

# 4. VISUALIZACIÓN (El gráfico para la memoria)
plt.figure(figsize=(12, 6))
# Creamos un gráfico de barras
plt.barh(df_top['Territori'], df_top['Crecimiento_%'], color='salmon')
plt.xlabel(f'Subida del precio (%) entre {anio_inicio}-{anio_fin}')
plt.title('Top 10 Barrios con mayor Gentrificación (Velocidad de subida)')
plt.gca().invert_yaxis() # Para que el nº1 salga arriba
plt.tight_layout()

# Guardamos el gráfico en una imagen
plt.savefig('grafico_gentrificacion.png')
print("\n Gráfico guardado como 'grafico_gentrificacion.png'. Ábrelo para verlo.")

# 5. Guardar este análisis enriquecido
df.to_csv('datos_con_metricas.csv', sep=';', index=False, encoding='utf-8-sig')