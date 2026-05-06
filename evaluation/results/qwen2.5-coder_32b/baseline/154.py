import folium
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString
from geopandas import GeoDataFrame

# Пример данных (в реальном проекте данные будут загружены из внешних источников)
data = {
    'river': ['Shynzhaly', 'Shyzhyn'],
    'coordinates': [
        [[76.95, 42.85], [77.00, 42.90], [77.05, 42.95]],  # Примерные координаты для Шыңжалий
        [[77.10, 43.00], [77.15, 43.05], [77.20, 43.10]]   # Примерные координаты для Шызынь
    ],
    'flood_probability': [0.25, 0.35]  # Вероятность наводнений (примерные значения)
}

# Создание GeoDataFrame
gdf = GeoDataFrame(data, geometry=[LineString(coords) for coords in data['coordinates']])

# Функция для создания карты с отображением вероятности наводнений
def create_flood_map(gdf):
    # Создаем базовую карту
    m = folium.Map(location=[42.95, 77.05], zoom_start=10)
    
    # Добавляем линии рек на карту с цветовой кодировкой вероятности наводнений
    for _, row in gdf.iterrows():
        color = 'blue' if row['flood_probability'] < 0.3 else 'red'
        folium.PolyLine(
            locations=row['geometry'].coords,
            color=color,
            weight=5,
            opacity=1
        ).add_to(m)
        
        # Добавляем метку с вероятностью наводнений
        centroid = row['geometry'].centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=f"Вероятность наводнений: {row['flood_probability']:.2f}",
            icon=folium.Icon(color='black', icon_color=color)
        ).add_to(m)
    
    return m

# Создаем и сохраняем карту
m = create_flood_map(gdf)
m.save("154.html")