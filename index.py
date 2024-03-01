import requests
import pandas as pd
import mysql.connector
import json
from flask_cors import CORS

conexion = mysql.connector.connect(user='root', 
                                   password='rootPassword',
                                   host='localhost', 
                                   database='productsTestDB', 
                                   port='3306')
cursor = conexion.cursor()

# Realizar una consulta SQL
cursor.execute("SELECT * FROM netflix_titles")

# Obtener todos los resultados
resultados = cursor.fetchall()

# Obtener los nombres de las columnas
columnas = cursor.description
nombres_de_columnas = [columna[0] for columna in columnas]

# Convertir los resultados a un formato JSON
# Crear una lista de diccionarios, donde cada diccionario representa una fila
datos_json = [dict(zip(nombres_de_columnas, fila)) for fila in resultados]

# Convertir la lista de diccionarios a una cadena JSON
data = json.dumps(datos_json, indent=4)

def convertir_respuesta_api(respuesta_api):
    # Procesa la respuesta de la API y la convierte en un diccionario
    data = {}
    for producto in respuesta_api:
        for clave, valor in producto.items():
            if clave in data:
                data[clave].append(valor)
            else:
                data[clave] = [valor]
    return data

# URL de la API donde quieres enviar la solicitud POST
url = 'http://127.0.0.1:5000/recommendations'

# Define una función para solicitar la entrada del usuario y enviar la solicitud POST
def solicitar_recomendaciones():
    product_user_input = input("Ingrese una camiseta o marca: ")
    response = requests.get('http://localhost:3004/data')
    data = convertir_respuesta_api(response.json())
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Add a 'Relevance' column with default values of 0 if it doesn't already exist
    if 'Relevance' not in df.columns:
        df['Relevance'] = 0
    
    # Convert the DataFrame back to a dictionary format expected by your Flask API
    data = df.to_dict('records')  # Converts the DataFrame back to a list of dictionaries
    
    dataJSON = {
        'user_name': 'usuario123',
        'product_user_input': product_user_input,
        'product_ID': 'Product_Name',
        'dataset': data  # Now includes 'Relevance' column
    }

    # Initial POST request
    response = requests.post(url, json=dataJSON)
    if response.status_code == 200:
        recommended_shirts = pd.DataFrame(response.json())
        print("Recomendaciones de camisetas:")
        print(recommended_shirts)

        # # Assuming products have a unique identifier column, e.g., 'Product_ID'
        # chosen_product_id = input("Seleccione el ID del producto de la lista: ")

        # # Assuming you also send back IDs of all recommended products as previous recommendations
        # previous_recommendations = recommended_shirts['Product_ID'].tolist()

        # # Prepare and send the follow-up POST request with chosen_product_id and previous_recommendations
        # follow_up_dataJSON = {
        #     'user_name': 'usuario123',
        #     'chosen_product_id': chosen_product_id,
        #     'previous_recommendations': previous_recommendations,
        #     'dataset': data  # Or however you manage the dataset across requests
        # }

        # response = requests.post(url, json=follow_up_dataJSON)
        # if response.status_code == 200:
        #     new_recommended_shirts = pd.DataFrame(response.json())
        #     print("Nuevas recomendaciones de camisetas basadas en su elección:")
        #     print(new_recommended_shirts)
        # else:
        #     print("Error al enviar la segunda solicitud:", response.status_code)
    else:
        print("Error al enviar la solicitud:", response.status_code)

# Assuming 'url' is defined as before
solicitar_recomendaciones()