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
    products = soup.find_all('div',class_='product-card')
    print(products)
    
    for product in products:
        product_name=product.product.div.text
        print(product_name)
        
    