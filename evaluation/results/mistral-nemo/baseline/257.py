import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import folium

# 1. Подготовка данных
river_data = gpd.read_file('river.shp')  # Замените на путь к вашим данным о реке Баянколь
fields_data = gpd.read_file('fields.shp')  # Замените на путь к вашим данным о полях

# 2. Вычисление расстояния
def calculate_distance(row):
    geometry = row['geometry']
    river_geom = river_data.iloc[0]['geometry']
    distance = geometry.distance(river_geom)
    return distance

fields_data['distance_to_river'] = fields_data.apply(calculate_distance, axis=1)

# 3. Определение потребности в поливе
def calculate_water_needs(row):
    distance = row['distance_to_river']
    water_level = river_data.iloc[0]['water_level']  # Замените на путь к данным о уровне воды в реке Баянколь

    if water_level < 5:
        return (distance * 1.5) + 10
    elif water_level >= 5 and water_level <= 10:
        return distance + 5
    else:
        return distance

fields_data['water_needs'] = fields_data.apply(calculate_water_needs, axis=1)

# 4. Визуализация результатов
m = folium.Map(location=[river_data.iloc[0].geometry.y, river_data.iloc[0].geometry.x], zoom_start=12)

for _, row in fields_data.iterrows():
    geometry = Point(row.geometry.x, row.geometry.y)
    water_needs = row['water_needs']
    color = 'green' if water_needs < 50 else 'yellow' if water_needs >= 50 and water_needs <= 100 else 'red'
    folium.CircleMarker(location=[geometry.y, geometry.x], radius=5, color=color).add_to(m)

m.save("257.html")