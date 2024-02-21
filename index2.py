from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)


class SimilarityBasedRecommendation:
    def __init__(self, dataset):
        self.dataset = dataset

    def recommend(self, user_input):
        # Convertir la entrada del usuario a minúsculas para una comparación insensible a mayúsculas y minúsculas
        user_input = user_input.lower()

        # Crear un DataFrame vacío para almacenar las recomendaciones
        recommendations_df = pd.DataFrame(columns=self.dataset.columns)

        # Iterar sobre las filas del conjunto de datos
        for index, row in self.dataset.iterrows():
            # Convertir los valores de la fila a minúsculas para una comparación insensible a mayúsculas y minúsculas
            row_values = row.astype(str).str.lower()

            # Buscar coincidencias con la entrada del usuario en la fila actual
            if row_values.str.contains(user_input, case=False).any():
                # Agregar la fila completa al DataFrame de recomendaciones
                recommendations_df = pd.concat([recommendations_df, row.to_frame().T], ignore_index=True)

        return recommendations_df.head(5)


    def update_relevance(self, chosen_shirt, name_products_input):
        # Aumentamos la relevancia de la prenda escogida en 1
        self.dataset.loc[self.dataset[name_products_input] == chosen_shirt, 'Relevance'] += 1

        # Si la relevancia alcanza 100, la dejamos ahí
        self.dataset.loc[self.dataset['Relevance'] > 100, 'Relevance'] = 100
        

    
# Crea una instancia de la clase ShirtRecommendationFromDataset

shirt_rec_from_dataset = None

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    global shirt_rec_from_dataset

    # Recibe los datos del cuerpo de la solicitud POST
    data = request.get_json()
    

    if 'chosen_shirt' in data:
        # Si se proporciona 'chosen_shirt', significa que el usuario ha seleccionado un producto
        chosen_shirt = data['chosen_shirt']
        user_name = data['user_name']
        name_products_input = data['name_products_input']

        # Actualiza la relevancia del producto seleccionado
        shirt_rec_from_dataset.update_relevance(chosen_shirt, name_products_input)

        # Obtén nuevas recomendaciones basadas en el producto seleccionado
        new_recommendations = shirt_rec_from_dataset.recommend(chosen_shirt)

        print(new_recommendations)
        # Devuelve las nuevas recomendaciones al usuario
        return new_recommendations.to_json(), 200
    else:
        # Si no se proporciona 'chosen_shirt', realiza la lógica de recomendación inicial
        user_name = data['user_name']
        product_user_input = data['product_user_input']
        name_products_input = data['name_products_input']
        dataset = data['dataset']
        df = pd.DataFrame(dataset)

        # Crea una instancia de la clase ShirtRecommendationFromDataset con el DataFrame df
        shirt_rec_from_dataset = SimilarityBasedRecommendation(df)

        # Realiza la lógica de recomendación inicial
        recommended_shirts = shirt_rec_from_dataset.recommend(product_user_input)


        print(recommended_shirts)
        # Devuelve las recomendaciones iniciales al usuario
        return recommended_shirts.to_json(), 200

if __name__ == '__main__':
    app.run(debug=True)
