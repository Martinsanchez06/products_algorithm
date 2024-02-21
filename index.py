import requests
import pandas as pd

# URL de la API a la que deseas hacer el GET
url = 'http://localhost:3004/data'

# Realizar la solicitud GET
response = requests.get(url)

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

# Convierte la respuesta de la API en un diccionario de datos
data = convertir_respuesta_api(response.json())

# URL de la API donde quieres enviar la solicitud POST
url = 'http://127.0.0.1:5000/recommendations'

# Define una función para solicitar la entrada del usuario y enviar la solicitud POST
def solicitar_recomendaciones():
    product_user_input = input("Ingrese una camiseta o marca: ")

    # Datos que quieres enviar a la API
    dataJSON = {
        'user_name': 'usuario123',
        'product_user_input': product_user_input,
        'name_products_input': 'Product_Name',
        'dataset': data
    }

    # Enviar la solicitud POST a la API
    response = requests.post(url, json=dataJSON)

    # Verificar la respuesta de la API
    if response.status_code == 200:
        recommended_shirts = pd.DataFrame(response.json())
        print("Recomendaciones de camisetas:")
        print(recommended_shirts)

        # Solicitar al usuario que seleccione un producto de la lista
        chosen_product = input("Seleccione un producto de la lista (escriba el nombre exacto): ")

        # Enviar una segunda solicitud con el producto seleccionado
        dataJSON['chosen_shirt'] = chosen_product
        response = requests.post(url, json=dataJSON)

        # Verificar la respuesta de la segunda solicitud
        if response.status_code == 200:
            new_recommended_shirts = pd.DataFrame(response.json())
            print("Nuevas recomendaciones de camisetas:")
            print(new_recommended_shirts)
        else:
            print("Error al enviar la segunda solicitud:", response.status_code)
    else:
        print("Error al enviar la solicitud:", response.status_code)

# Llama a la función para iniciar el flujo de recomendaciones
solicitar_recomendaciones()
