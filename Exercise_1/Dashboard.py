import streamlit as st
import requests
import pandas as pd
import json

# URL de la API del INEGI
api_key = 'cc1b4dab-8051-3e70-b972-3d32758dcd7b'
url = f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/00/true/BISE/2.0/{api_key}?type=json'

# Realiza la solicitud GET a la API
response = requests.get(url)

# Imprime el estado de la respuesta y el contenido completo
print('Estado de la respuesta:', response.status_code)
print('Contenido de la respuesta:', response.text)

if response.status_code == 200:
    try:
        data = response.json()
        # Convierte el JSON en un DataFrame
        df = pd.json_normalize(data['Series'])

        # Imprime el DataFrame
        print(df)
    except json.decoder.JSONDecodeError:
        print("La respuesta no es un JSON válido")
else:
    print(f'Error: {response.status_code}')