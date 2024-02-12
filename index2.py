import pandas as pd

class ShirtRecommendationFromDataset:
    def __init__(self, dataset):
        self.dataset = dataset

    def fit(self):
        # Agregamos una nueva columna de "Relevancia" inicializada en 0 para todas las prendas
        self.dataset['Relevancia'] = 0

    def recommend(self, user_input):
        recommended_shirts = []

        # Filtramos el dataset basado en la entrada del usuario en las columnas "Nombre" y "Marca"
        filtered_dataset = self.dataset[(self.dataset['Nombre'].str.contains(user_input, case=False)) | (self.dataset['Marca'].str.contains(user_input, case=False))]

        # Ordenamos el dataset filtrado por alguna métrica de relevancia, en este caso, por la columna 'Relevancia' de manera descendente
        sorted_dataset = filtered_dataset.sort_values(by='Relevancia', ascending=False)

        # Tomamos las primeras 5 filas del dataset ordenado como nuestras recomendaciones
        recommended_shirts = sorted_dataset.head(5)

        # Devolvemos las camisetas recomendadas al usuario
        return recommended_shirts

    def update_relevance(self, chosen_shirt):
        # Aumentamos la relevancia de la prenda escogida en 1
        self.dataset.loc[self.dataset['Nombre'] == chosen_shirt, 'Relevancia'] += 1

        # Si la relevancia alcanza 100, la dejamos ahí
        self.dataset.loc[self.dataset['Relevancia'] > 100, 'Relevancia'] = 100

# Creamos un conjunto de datos representado como un DataFrame de pandas
data = {
        'Nombre': ['Camiseta Azul', 'Camiseta Roja', 'Polo Blanco', 'Camisa Negra', 'Blusa Amarilla', 'Camiseta Verde', 'Pantalón Azul', 'Shorts Rojos', 'Chaqueta Negra', 'Bufanda Gris', 'Vestido Floral', 'Sweater Azul', 'Abrigo Negro', 'Camiseta Rayada', 'Blusa Blanca', 'Zapatos Negros', 'Zapatos Blancos', 'Botas Marrones', 'Gorra Roja', 'Gorra Negra', 'Falda Plisada', 'Jeans Azules', 'Calcetines Blancos', 'Calcetines Negros', 'Chaleco Gris', 'Pantalón Corto Verde', 'Camiseta Manga Larga', 'Jersey Rosa', 'Bufanda Roja', 'Gorro de Lana', 'Pantalón Deportivo', 'Sudadera Gris', 'Chaquetón Azul', 'Abrigo de Piel', 'Parka Verde', 'Pantalón Cargo', 'Cazadora Vaquera', 'Vestido de Noche', 'Blusa de Encaje', 'Chaleco Vaquero', 'Bañador Negro', 'Sombrero de Paja', 'Blazer Gris', 'Sudadera con Capucha', 'Pantalones de Cuero', 'Camiseta de Algodón', 'Vestido Elegante', 'Zapatillas Deportivas', 'Falda de Cuadros', 'Polo arcoiris'], 
        'Marca': ['Marca2', 'Marca6', 'Marca6', 'Marca6', 'Marca2', 'Marca4', 'Marca3', 'Marca6', 'Marca2', 'Marca6', 'Marca6', 'Marca6', 'Marca3', 'Marca1', 'Marca6', 'Marca1', 'Marca7', 'Marca2', 'Marca6', 'Marca3', 'Marca3', 'Marca6', 'Marca6', 'Marca7', 'Marca5', 'Marca5', 'Marca7', 'Marca7', 'Marca4', 'Marca4', 'Marca6', 'Marca7', 'Marca4', 'Marca1', 'Marca7', 'Marca1', 'Marca5', 'Marca6', 'Marca6', 'Marca2', 'Marca3', 'Marca4', 'Marca2', 'Marca7', 'Marca3', 'Marca5', 'Marca1', 'Marca2', 'Marca7', 'Marca5']}

# Creamos un DataFrame de pandas a partir del conjunto de datos
df = pd.DataFrame(data)

# Creamos una instancia de la clase ShirtRecommendationFromDataset y le pasamos nuestro DataFrame como argumento
shirt_rec_from_dataset = ShirtRecommendationFromDataset(df)

# Llamamos al método fit para inicializar la relevancia de las prendas
shirt_rec_from_dataset.fit()

# Bucle principal
while True:
    # Entrada del usuario
    user_input = input("Ingrese una camiseta o marca: ")

    # Recomendamos camisetas similares a la entrada del usuario
    recommended_shirts = shirt_rec_from_dataset.recommend(user_input)

    # Mostramos las camisetas recomendadas al usuario
    print("\nCamisetas recomendadas para '{}':".format(user_input))
    print(recommended_shirts[['Nombre', 'Marca']])  # Mostramos solo las columnas "Nombre" y "Marca" de las recomendaciones

    # El usuario elige una prenda entre las recomendadas
    chosen_shirt = input("Seleccione una prenda de la lista (escriba el nombre exacto): ")

    # Actualizamos la relevancia de la prenda elegida
    shirt_rec_from_dataset.update_relevance(chosen_shirt)

    # Mostramos el estado actual de las relevancias
    print("\nEstado actual de relevancias:")
    print(shirt_rec_from_dataset.dataset[['Nombre', 'Relevancia']])  # Mostramos el nombre y la relevancia de todas las prendas

    # Si se desea salir del bucle, se escribe "exit"
    if chosen_shirt.lower() == 'exit':
        break
