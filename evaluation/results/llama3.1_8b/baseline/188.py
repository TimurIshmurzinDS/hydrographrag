import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Сбор данных о характеристиках рек Шарын и Уржар
data = {
    'Река': ['Шарын', 'Уржар'],
    'Длина (км)': [200, 150],
    'Ширина (м)': [10, 15],
    'Скорость течения (м/с)': [0.5, 1.2],
    'Температура воды (°C)': [12, 15],
    'Уровень кислорода (%)': [80, 90]
}

df = pd.DataFrame(data)

# Анализ данных для определения ключевых факторов
import numpy as np

# Вычисляем средние значения для каждого реки
mean_values = df.groupby('Река').mean()

# Определяем корреляцию между факторами
corr_matrix = mean_values.corr()

# Создаем геоспациальные модели для прогнозирования экологического статуса
from sklearn.ensemble import RandomForestRegressor

X = corr_matrix.drop(['Шарын'], axis=1)
y = mean_values['Шарын']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Визуализация результатов на карте
m = Map(location=[50.0, 70.0], zoom_start=6)

for index, row in df.iterrows():
    if row['Река'] == 'Шарын':
        marker = Marker([row['Длина (км)'], row['Ширина (м)']], popup=f"Экологический статус: {model.predict(X.loc[['Уржар']])}").add_to(m)
    else:
        circle_marker = CircleMarker([row['Длина (км)'], row['Ширина (м)']], radius=10, color='red', fill=True).add_to(m)

m.save("188.html")