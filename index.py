import requests
import pandas as pd

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
      'user_name': "usuario123",
      'product_user_input': product_user_input,
      'product_ID': 'product_name',
      'dataset': data,
      'price_column': "price",
      'category_discounts': {
        "Carlton London": [5, 20],
        "Denver": [5, 20],
        "Engage": [5, 20],
        "Envy": [5, 20],
        "FOGG": [5, 20],
        "KS WOMAN": [5, 20],
        "LA' French": [5, 20],
        "Ahava": [5, 20],
        "Alpha Skin Care": [5, 20],
        "American Crew": [5, 20],
        "Ariana Grande": [5, 20],
        "Babo Botanicals": [5, 20],
        "Baxter of California": [5, 20],
        "Beast": [5, 20],
        "Beekman 1802": [5, 20],
        "Bliss": [5, 20],
        "boscia": [5, 20],
        "Briogeo": [5, 20],
        "Bushbalm": [5, 20],
        "Buttah Skin": [5, 20],
        "Cetaphil": [5, 20],
        "Clarins": [5, 20],
        "Clinique": [5, 20],
        "Coco & Eve": [5, 20],
        "Da Bomb": [5, 20],
        "Daily Concepts": [5, 20],
        "Dermalogica": [5, 20],
        "Differin": [5, 20],
        "Dionis": [5, 20],
        "Dr Teal's": [5, 20],
      },
    }

    # Initial POST request
    response = requests.post(url, json=dataJSON)
    if response.status_code == 200:
        recommended_shirts = pd.DataFrame(response.json())
        print("Recomendaciones de camisetas:")
        print(recommended_shirts)
    else:
        print("Error al enviar la solicitud:", response.status_code)

# Assuming 'url' is defined as before
solicitar_recomendaciones()