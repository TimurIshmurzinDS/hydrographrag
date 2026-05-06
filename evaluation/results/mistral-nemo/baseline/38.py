import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных
data = {
    'id': [1, 2, 3, 4, 5],
    'geometry': [
        Point(76.9083, 43.2566),
        Point(76.9122, 43.2589),
        Point(76.9161, 43.2612),
        Point(76.9200, 43.2635),
        Point(76.9239, 43.2658)
    ],
    'water_quality': [6, 7, 5, 8, 6],
    'soil_pollution': [4, 5, 3, 4, 5],
    'air_pollution': [3, 4, 2, 3, 4],
    'human_activity': [2, 3, 1, 2, 3]
}

# Шаг 2: Подготовка данных
gdf = gpd.GeoDataFrame(data)
gdf['risk'] = (gdf['water_quality'] + gdf['soil_pollution'] + gdf['air_pollution'] + gdf['human_activity']) / 4

# Шаг 3: Анализ данных
# В этом примере мы просто вычисляем средний уровень риска для каждой точки.
# В реальной ситуации можно использовать более сложные методы анализа данных.

# Шаг 4: Визуализация результатов
m = folium.Map(location=[43.2566, 76.9083], zoom_start=12)

for idx, row in gdf.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=row['risk'] * 2,
        color='red',
        fill=True
    ).add_to(m)

m.save("38.html")