import pandas as pd
from folium import Map, Marker
import numpy as np

# Шаг 1: Сбор данных (предположим, что данные хранятся в файле 'karatal_data.csv')
data = pd.read_csv('karatal_data.csv')

# Шаг 2: Анализ данных
anomaly_threshold = 20  # Норма температуры воды
anomalies = data[data['temperature'] > anomaly_threshold]

# Шаг 3: Моделирование (предположим, что приготовление пасты невозможно при температуре выше 25°C)
def can_cook_pasta(temp):
    return temp <= 25

# Шаг 4: Визуализация
m = Map(location=[46.5, 76.0], zoom_start=10)

for index, row in anomalies.iterrows():
    lat, lon = row['latitude'], row['longitude']
    marker = Marker(location=[lat, lon], popup=f'Аномальная температура воды: {row["temperature"]}°C')
    if can_cook_pasta(row['temperature']):
        marker.add_child(folium.Div(style={'color': 'green'}, text='Можно приготовить пасту'))
    else:
        marker.add_child(folium.Div(style={'color': 'red'}, text='Нельзя приготовить пасту'))
    m.add_child(marker)

m.save("222.html")