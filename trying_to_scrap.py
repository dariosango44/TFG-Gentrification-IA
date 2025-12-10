#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 15:34:29 2025

@author: dariosango44
@description: le voy dando caña a la vaina bacana del tfg de info

"""

import requests
from lxml import html 
from bs4 import BeautifulSoup


with open('/Users/dariosango44/Documents/mis cosillas/prova_scrapping.html','r') as html_file:
    
    content=html_file.read()
    soup = BeautifulSoup(content,'lxml')
    #print(soup)
    product_cards = soup.find_all('div',{'class':'product-card'})
    
    print(f"El número de productos de la página es {len(product_cards)}\n")
    
    productos = []
    
    for i, product in enumerate(product_cards,1):
        print(f"\n{'-'*50}")
        print(f"PRODUCTO {i}:")
        print('-'*50)
        
        # 1 Nombre
        name_tag = product.find('div', class_='product-name')
        name = name_tag.text.strip() if name_tag else "N/A"
        print(f"Nombre: {name}")
        
        # 2 Emoji
        emoji_tag = product.find('div', class_='product-image')
        emoji = emoji_tag.text.strip() if emoji_tag else "N/A"
        print(f"Emoji: {emoji}")
        
        # 3 Categoría
        category_tag = product.find('div', class_='product-category')
        category = category_tag.text.strip() if category_tag else "N/A"
        print(f"Categoría: {category}")
        
        
        # 4 Descripción
        description_tag = product.find('div', class_='product-description')
        description = description_tag.text.strip() if description_tag else "N/A"
        print(f"Descripción: {description}")
        
        # 5 Precio
        price_tag = product.find('div', class_='product-price')
        price = name_tag.text.strip() if price_tag else "N/A"
        print(f"Precio: {price}")
        
        # 5bis Precio original
        originalprice_tag = product.find('div', class_='product-price')
        originalprice = name_tag.text.strip() if originalprice_tag else "N/A"
        print(f"Precio original: {originalprice}")
        
        # 6 Descuento
        discount_tag = product.find('div', class_='discount-badge')
        discount = discount_tag.text.strip('-') if discount_tag else "N/A"
        print(f"Descuento: {discount}")
        
        # 7 Estado
        status_tag = product.find('div', class_='stock-status stock-available')
        status = status_tag.text.strip() if status_tag else "N/A"
        print(f"Estado: {status}")
        
        # 8 Rating
        rating_tag = product.find('div',class_='rating')
        rating = rating_tag.text.strip() if rating_tag else "N/A"
        print(f"Rating: {rating}")
        
        # Almacenar en diccionario
        producto_dict = {
            'numero': i,
            'emoji': emoji,
            'nombre': name,
            'categoria': category,
            'descripcion': description,
            'precio_actual': price,
            'precio_original': originalprice if originalprice != "N/A" else None,
            'descuento': discount if discount != "Sin descuento" else None,
            'stock': status,
            'rating': rating
        }
        productos.append(producto_dict)
    
print(productos)
    #products_name = soup.find_all('div',{'class':'product-name'})
    #products_emojis = soup.find_all('div',{'class':'product-image'})
    
    #print(products_name)
    #print(products_emojis)
    
    
    