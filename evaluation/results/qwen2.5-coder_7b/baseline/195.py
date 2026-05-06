import pandas as pd
import numpy as np
from folium import Map, TileLayer, Marker, Popup
from folium.plugins import HeatMap

# Пример данных: координаты участков и данные о поливе
data = {
    'latitude': [51.234, 51.235, 51.236],
    'longitude': [76.345, 76.346, 76.347],
    'water_volume': [1000, 1500, 2000],  # объем поливной воды в литрах
    'nitrate_content': [10, 15, 20]  # содержание нитратов в мг/л
}

df = pd.DataFrame(data)

# Создаем карту
m = Map(location=[51.234, 76.345], zoom_start=13, tiles='OpenStreetMap')

# Добавляем маркеры с данными полива
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Водоем: {index}<br>Объем воды: {row['water_volume']} л<br>Содержание нитратов: {row['nitrate_content']} мг/л",
        icon=folium.Icon(color='blue', icon='drop')
    ).add_to(m)

# Добавляем тепловую карту для визуализации плотности полива
heat_data = [[row['latitude'], row['longitude'], row['water_volume']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# Сохраняем карту
m.save("195.html")