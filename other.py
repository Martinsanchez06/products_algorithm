import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('./Balaji Fast Food Sales.csv')

# Eliminar filas con nombres de ítems duplicados y limitar a 100 productos únicos
df_unique_names_limited = df.head(100)

# Preparar instrucciones SQL para los primeros 100 productos únicos
insert_statements_limited = []
for index, row in df_unique_names_limited.iterrows():
    # Convertir todos los valores a string y manejar correctamente los valores nulos y las comillas simples
    values = [f"'{str(value).replace('\'', '\'\'')}'" if pd.notnull(value) else 'NULL' for value in row]
    insert_statement = f"INSERT INTO BalajiFastFoodSales (order_id, date, item_name, item_type, item_price, quantity, transaction_amount, transaction_type, received_by, time_of_sale) VALUES ({', '.join(values)});"
    insert_statements_limited.append(insert_statement)

print(len(insert_statements_limited), insert_statements_limited[:100])  # Mostrar la cantidad y las primeras 5 instrucciones como muestra
