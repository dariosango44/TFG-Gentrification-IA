#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 12:55:57 2025

@author: dariosango44
@name: idealista_scraper
@description: begining with the scrap to idealista...

"""


import pandas as pd
import numpy as np

# Ja em posaré amb sa extracció de dades
# Hores d'ara, li fotré canya a aprendre el processament d'aquestes


archivo = 'data_table.csv'


try:

    df = pd.read_csv(archivo) 
    
    print(df.head())
    df = df.replace('-', np.nan) # delete -'s. Write Not a Number (NaN)
    print(df.head())
    
    
    # Seleccionamos todas las columnas menos las dos primeras (Territori, Tipus)
    columnas_anos = df.columns[2:] 
    
    for col in columnas_anos:
        df[col] = pd.to_numeric(df[col])
        
     # 4. MOSTRAR RESULTADOS
    print("\n--- VISTA PREVIA DE LOS DATOS LIMPIOS ---")
    print(df.head())

    print("\n--- ESTADÍSTICAS RÁPIDAS ---")
    # Vamos a ver cuál es el precio máximo registrado en 2023 (si hay datos)
    if '2023' in df.columns:
        barrio_caro = df.loc[df['2023'].idxmax()]
        print(f"El barrio más caro en 2023 fue: {barrio_caro['Territori']} con {barrio_caro['2023']} €/m2")

    # 5. GUARDAR EL RESULTADO LIMPIO
    # Guardamos esto en un nuevo CSV para usarlo luego en la App sin tener que limpiar cada vez
    df.to_csv('datos_limpios_final.csv', sep=';', index=False, encoding='utf-8-sig')
    
    print("\nDatos limpios guardados en 'datos_limpios_final.csv'")

except FileNotFoundError:
    print("ERROR: No encuentro 'datos_historicos_alquiler.csv'. Asegúrate de haberlo creado y pegado el texto.")
    
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")