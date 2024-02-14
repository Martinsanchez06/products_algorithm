import pandas as pd
import requests

# URL de la API a la que deseas hacer el GET
url = 'http://localhost:3004/data'

# Realizar la solicitud GET
response = requests.get(url)

def convertir_respuesta_api(respuesta_api):
    # Inicializar un diccionario vacío para almacenar los datos
    data = {}

    # Iterar sobre los elementos de la respuesta de la API
    for producto in respuesta_api:
        # Iterar sobre las claves y valores de cada producto
        for clave, valor in producto.items():
            # Verificar si la clave ya existe en el diccionario data
            if clave in data:
                # Si la clave ya existe, agregar el valor a la lista correspondiente
                data[clave].append(valor)
            else:
                # Si la clave no existe, crear una nueva lista con el valor
                data[clave] = [valor]

    return data

# Creamos un conjunto de datos representado como un DataFrame de pandas
data = convertir_respuesta_api(response.json())

class ShirtRecommendationFromDataset:
    def __init__(self, dataset):
        self.dataset = dataset

    def recommend(self, product_user_input):
        recommended_shirts = []

        # Filtramos el dataset basado en la entrada del usuario en las columnas "Nombre" y "Marca"
        filtered_dataset = self.dataset  # Inicializamos el dataset filtrado con el dataset completo
        for key in self.dataset.keys():
            if isinstance(self.dataset[key], str):  # Solo aplicamos a las llaves que contienen cadenas de texto
                filtered_dataset = filtered_dataset[filtered_dataset[key].str.contains(product_user_input, case=False)]

        # Ordenamos el dataset filtrado por alguna métrica de relevancia, en este caso, por la columna 'Relevancia' de manera descendente
        if not filtered_dataset.empty:  # Verificamos si el dataset filtrado no está vacío
        #     sorted_dataset = filtered_dataset.sort_values(by='Relevancia', ascending=False)

        #     # Tomamos las primeras 5 filas del dataset ordenado como nuestras recomendaciones
        #     recommended_shirts = sorted_dataset.head(5)
        # else:
            recommended_shirts = filtered_dataset.head(5) 

        # Devolvemos las camisetas recomendadas al usuario
        return recommended_shirts

    def update_relevance(self, chosen_shirt):
        # Aumentamos la relevancia de la prenda escogida en 1
        self.dataset.loc[self.dataset[name_products_input] == chosen_shirt, 'Relevance'] += 1

        # Si la relevancia alcanza 100, la dejamos ahí
        self.dataset.loc[self.dataset['Relevance'] > 100, 'Relevance'] = 100


# Inicializamos un array para almacenar las llaves
keys_array = []

# Iteramos sobre las llaves del diccionario y las agregamos al array
for key in data.keys():
    keys_array.append(key)
    
# Creamos un DataFrame de pandas a partir del conjunto de datos
df = pd.DataFrame(data)

# Creamos una instancia de la clase ShirtRecommendationFromDataset y le pasamos nuestro DataFrame como argumento
shirt_rec_from_dataset = ShirtRecommendationFromDataset(df)

# Bucle principal
while True:
    # Entrada del usuario
        product_user_input = input("Ingrese una camiseta o marca: ")
        name_products_input = input("Nombre de la columna de los nombres de productos: ")
        

    # Recomendamos camisetas similares a la entrada del usuario
        recommended_shirts = shirt_rec_from_dataset.recommend(product_user_input)

        # Mostramos las camisetas recomendadas al usuario
        print("\nCamisetas recomendadas para '{}':".format(product_user_input))
        print(recommended_shirts[keys_array])  # Mostramos solo las columnas "Nombre" y "Marca" de las recomendaciones

    # El usuario elige una prenda entre las recomendadas
        chosen_shirt = input("Seleccione una prenda de la lista (escriba el nombre exacto): ")

        # Actualizamos la relevancia de la prenda elegida
        shirt_rec_from_dataset.update_relevance(chosen_shirt)

        # Mostramos el estado actual de las relevancias
        print("\nEstado actual de relevancias:")
        print(shirt_rec_from_dataset.dataset[keys_array])  # Mostramos el nombre y la relevancia de todas las prendas

        # Si se desea salir del bucle, se escribe "exit"
        if chosen_shirt.lower() == 'exit':
            break
