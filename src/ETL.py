import os
import pandas as pd
import sqlite3

file_path = './utils/data-GlobalMobilityApex.csv'
if not os.path.exists(file_path):
    print(f"El archivo no existe en la ruta: {file_path}")
else:
    print(f"Archivo encontrado: {file_path}")
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

print("Nombres de las columnas en el DataFrame:")
print(df.columns)


df['quantity'] = df['quantity'].fillna(0).astype(int)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

median_prices = df.groupby('category')['price'].transform('median')
df['price'] = df['price'].fillna(median_prices)

df = df.dropna(subset=['quantity', 'price'], how='any')

df['total_sales'] = df['quantity'] * df['price']

df['date'] = pd.to_datetime(df['date'])

df['day_of_week'] = df['date'].dt.day_name()

df['high_volume'] = df['quantity'] > 10

conn = sqlite3.connect('sales_dashboard.db')

df.to_sql('Transactions', conn, if_exists='replace', index=False)

aggregated_metrics = df.groupby('category').agg(
    total_revenue=('total_sales', 'sum'),
    average_price=('price', 'mean'),
    highest_quantity=('quantity', 'max')
).reset_index()
aggregated_metrics.to_sql('AggregatedMetricsByCategory', conn, if_exists='replace', index=False)


print("Metricas agregadas por categoria:")
print(pd.read_sql_query("SELECT * FROM AggregatedMetricsByCategory", conn))

conn.close()