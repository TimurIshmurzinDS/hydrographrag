import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Шаг 1: Сбор данных (пример синтетических данных)
data = {
    'year': [2015, 2016, 2017, 2018, 2019, 2020, 2021],
    'migrants_count': [1000, 1200, 1300, 1400, 1500, 1600, 1700],
    'latitude': [55.7558, 55.7558, 55.7558, 55.7558, 55.7558, 55.7558, 55.7558],
    'longitude': [37.6173, 37.6173, 37.6173, 37.6173, 37.6173, 37.6173, 37.6173]
}
df = pd.DataFrame(data)

# Шаг 2: Обработка данных
df['migrants_count'] = df['migrants_count'].fillna(method='ffill')

# Шаг 3: Анализ временных рядов
result = seasonal_decompose(df['migrants_count'], model='additive', period=1)
predicted_next_year = result.trend.iloc[-1] + result.seasonal.iloc[-1]

# Шаг 4: Пространственное моделирование (пример кластеризации)
kmeans = KMeans(n_clusters=2, random_state=0).fit(df[['latitude', 'longitude']])
df['cluster'] = kmeans.labels_

# Предсказание следующей волны миграции
next_year_data = {
    'year': [2022],
    'migrants_count': [predicted_next_year],
    'latitude': [55.7558],  # Примерные координаты
    'longitude': [37.6173],  # Примерные координаты
    'cluster': kmeans.predict([[55.7558, 37.6173]])[0]
}
next_year_df = pd.DataFrame(next_year_data)

# Шаг 5: Визуализация результатов
m = folium.Map(location=[55.7558, 37.6173], zoom_start=12)
for _, row in df.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['migrants_count'] / 100,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

for _, row in next_year_df.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['migrants_count'] / 100,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# Сохранение карты
m.save("278.html")