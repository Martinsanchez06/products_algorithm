import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

class EnhancedSimilarityRecommendation:
    def __init__(self, dataset, category_discounts):
        self.dataset = dataset
        if 'Relevance' not in self.dataset.columns:
            self.dataset['Relevance'] = pd.Series(0, index=self.dataset.index)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.dataset.fillna('', inplace=True)
        self.update_combined_features()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.dataset['combined_features'])
        self.category_discounts = category_discounts
        self.add_category_based_discounts()

    def find_similar_products(self, user_input, product_ID_column):
        user_input_tfidf = self.vectorizer.transform([user_input.lower()])
        similarity_scores = cosine_similarity(user_input_tfidf, self.tfidf_matrix)[0]

        # Ajustar los puntajes de similitud para excluir el producto seleccionado
        self.dataset['similarity_score'] = similarity_scores
        selected_product_index = self.dataset.index[self.dataset[product_ID_column].str.lower() == user_input.lower()]
        self.dataset.loc[selected_product_index, 'similarity_score'] = -1

        adjusted_scores = self.dataset['similarity_score'] * (1 + self.dataset['Relevance'] / 100)
        top_indices = adjusted_scores.nlargest(4).index  # Obtiene los 4 más altos incluyendo el seleccionado
        recommendations = self.dataset.loc[top_indices]
        recommendations = recommendations[recommendations.index.isin(selected_product_index) == False]  # Excluye el seleccionado

        # Incrementar la relevancia para el producto seleccionado y recomendados
        self.update_relevance([user_input], product_ID_column, increment=5)  # Incremento mayor para el seleccionado
        recommended_product_ids = recommendations[product_ID_column].tolist()
        self.update_relevance(recommended_product_ids, product_ID_column, increment=2)  # Incremento menor para recomendados

        self.update_combined_features()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.dataset['combined_features'])

        return recommendations.head(3), self.dataset  # Devuelve solo los 3 primeros recomendados

    
    def add_category_based_discounts(self):
        self.dataset['Descuentos'] = 0  # Inicializar la columna de descuentos con ceros.
        for category, discount_info in self.category_discounts.items():
            category_indices = self.dataset[self.dataset['brand'] == category].index
            
            for idx in category_indices:
                relevance = self.dataset.at[idx, 'Relevance']
                if isinstance(discount_info, (list, tuple)) and len(discount_info) == 2:
                    # Ajustar ambos, el mínimo y el máximo del rango de descuento, basándonos en la relevancia.
                    adjusted_min_discount = discount_info[0] + (discount_info[0] * relevance / 100)
                    adjusted_max_discount = discount_info[1] + (discount_info[1] * relevance / 100)
                    adjusted_min_discount, adjusted_max_discount = min(adjusted_min_discount, 100), min(adjusted_max_discount, 100)
                    self.dataset.at[idx, 'Descuentos'] = np.random.randint(adjusted_min_discount, adjusted_max_discount + 1)
                elif isinstance(discount_info, int):
                    adjusted_discount = discount_info + (discount_info * relevance / 100)
                    adjusted_discount = min(adjusted_discount, 100)
                    self.dataset.at[idx, 'Descuentos'] = adjusted_discount



    def apply_relevance_based_discounts(self):
        # Asegurar que los valores en 'price', 'Descuentos', y 'Relevance' sean numéricos
        self.dataset['price'] = pd.to_numeric(self.dataset['price'], errors='coerce').fillna(0)
        self.dataset['Descuentos'] = pd.to_numeric(self.dataset['Descuentos'], errors='coerce').fillna(0)
        self.dataset['Relevance'] = pd.to_numeric(self.dataset['Relevance'], errors='coerce').fillna(0)

        # Definir una base para el ajuste de descuento basado en la relevancia
        # Por ejemplo, aplicar un aumento proporcional al porcentaje de relevancia
        self.dataset['Adjusted_Discount'] = self.dataset.apply(
            lambda row: min(row['Descuentos'] + (row['Relevance'] / 2), 100), axis=1
        )

        # Calcular 'Precio_Final' con los descuentos ajustados
        self.dataset['Precio_Final'] = self.dataset.apply(
            lambda row: round(row['price'] * (1 - row['Adjusted_Discount'] / 100), 2), axis=1
        )


        
    def update_relevance(self, product_ids, product_ID, increment=1):
        for product_id in product_ids:
            condition = (self.dataset[product_ID] == product_id)
            if condition.any():
                self.dataset.loc[condition, 'Relevance'] += increment
                # Asegúrate de no exceder un límite máximo de relevancia, si existe


    def update_combined_features(self):
        self.dataset['combined_features'] = self.dataset.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    dataset = pd.DataFrame(data['dataset'])
    category_discounts = data['category_discounts']  # Este deberá ser un diccionario
    rec_system = EnhancedSimilarityRecommendation(dataset, category_discounts)
    user_input = data['product_user_input']
    product_ID = data['product_ID']

    recommendations, updated_dataset = rec_system.find_similar_products(user_input, product_ID)

    recommended_products_json = json.loads(recommendations.to_json(orient='records'))
    all_products_json = json.loads(updated_dataset.to_json(orient='records'))

    response = {
        "recommended_products": recommended_products_json,
        "all_products": all_products_json
    }
    
    columnas_interes = ['Relevance', 'Descuentos']
    print(recommendations[columnas_interes])

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)

