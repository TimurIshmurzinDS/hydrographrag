import pandas as pd
from folium import Map, Marker, CircleMarker, Polygon, Icon
import numpy as np

# Шаг 1: Подготовка данных (предположим, что данные хранятся в DataFrames)
data_river = pd.DataFrame({
    'lat': [43.1234, 43.2345], 
    'lon': [76.5678, 76.6789],
    'width': [10, 15],
    'depth': [2, 3]
})

data_weather = pd.DataFrame({
    'rainfall': [20, 30],
    'temperature': [15, 18],
    'humidity': [60, 70]
})

# Шаг 2: Создание модели
def flood_model(rainfall, speed_flow, width, depth):
    # Простая модель для примера. На самом деле здесь должна быть более сложная логика.
    return rainfall * speed_flow / (width * depth)

# Шаг 3: Анализ данных и оценка риска паводка
risk_flood = data_weather['rainfall'] * data_river['speed_flow'] / (data_river['width'] * data_river['depth'])

# Визуализация на карте с помощью folium
m = Map(location=[43.2, 76.5], zoom_start=10)
for i in range(len(data_river)):
    marker = Marker(
        location=[data_river.loc[i, 'lat'], data_river.loc[i, 'lon']],
        popup=f'Риск паводка: {risk_flood.iloc[i]:.2f}',
        icon=Icon(color='red')
    ).add_to(m)

m.save("16.html")