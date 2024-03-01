from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

class EnhancedSimilarityRecommendation:
    def __init__(self, dataset):
        self.dataset = dataset
        if 'Relevance' not in self.dataset.columns:
            self.dataset['Relevance'] = pd.Series(0, index=self.dataset.index)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.dataset.fillna('', inplace=True)
        self.update_combined_features()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.dataset['combined_features'])

    def find_similar_products(self, user_input, product_ID):
        user_input_tfidf = self.vectorizer.transform([user_input.lower()])
        similarity_scores = cosine_similarity(user_input_tfidf, self.tfidf_matrix)[0]

        adjusted_scores = similarity_scores * (1 + self.dataset['Relevance'] / 100)
        top_indices = adjusted_scores.argsort()[-5:][::-1]
        recommendations = self.dataset.iloc[top_indices]

        # Corrección para manejar el incremento de relevancia
        self.update_relevance([user_input], product_ID, increment=3)  # Incrementa la relevancia del producto seleccionado por 3.

        recommended_product_ids = recommendations[product_ID].tolist()
        self.update_relevance(recommended_product_ids, product_ID, increment=2)  # Incrementa la relevancia de los productos recomendados por 2.

        self.update_combined_features()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.dataset['combined_features'])

        return recommendations, self.dataset

    def update_relevance(self, product_ids, product_ID, increment=1):
        # Asegura que los IDs del producto estén en formato adecuado para comparación
        product_ids = [str(pid) for pid in product_ids]  # Convierte a string si es necesario
        for product_id in product_ids:
            # Utiliza .any() para evitar errores al comparar con múltiples elementos
            condition = (self.dataset[product_ID] == product_id)
            if condition.any():
                self.dataset.loc[condition, 'Relevance'] += increment
                self.dataset.loc[self.dataset['Relevance'] > 100, 'Relevance'] = 100

    def update_combined_features(self):
        # Esta línea combina todos los valores de cada fila en una cadena, excluyendo valores NaN
        self.dataset['combined_features'] = self.dataset.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)


@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    dataset = pd.DataFrame(data['dataset'])
    rec_system = EnhancedSimilarityRecommendation(dataset)
    user_input = data['product_user_input']
    product_ID = data['product_ID']

    recommendations, updated_dataset = rec_system.find_similar_products(user_input, product_ID)

    # Convertir las cadenas JSON a objetos Python
    recommended_products_json = json.loads(recommendations.to_json(orient='records'))
    all_products_json = json.loads(updated_dataset.to_json(orient='records'))

    # Preparar y devolver la respuesta como JSON
    response = {
        "recommended_products": recommended_products_json,
        "all_products": all_products_json
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)