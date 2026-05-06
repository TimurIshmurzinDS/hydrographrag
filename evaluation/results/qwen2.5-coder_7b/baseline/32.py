import pandas as pd
import folium
from folium.plugins import HeatMap

# Пример данных о состоянии реки Талгар (замените на реальные данные)
data = {
    'latitude': [51.234, 51.235, 51.236, 51.237],
    'longitude': [76.890, 76.891, 76.892, 76.893],
    'water_level': [10, 11, 12, 13],
    'flow_speed': [2, 2.5, 3, 3.5],
    'pollutant_concentration': [0.5, 0.6, 0.7, 0.8]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[51.234, 76.890], zoom_start=13)

# Добавление маркеров с информацией о состоянии воды
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Уровень воды: {row['water_level']} м\nСкорость течения: {row['flow_speed']} м/с\nКонцентрация загрязнителя: {row['pollutant_concentration']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Добавление теплового картографа для концентрации загрязнителей
heat_data = [[row['latitude'], row['longitude'], row['pollutant_concentration']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# Сохранение карты
m.save("32.html")