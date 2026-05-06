import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть геоданные о реке Уржар и участках земель под сельское хозяйство.
# Также предположим, что мы знаем координаты точек полива.

# Создание примерных данных для реки Уржар
river_coords = [(48.3500, 39.2000), (48.3600, 39.2100), (48.3700, 39.2200)]
river_line = LineString(river_coords)
river_gdf = gpd.GeoDataFrame({'name': ['Уржар'], 'geometry': [river_line]}, crs="EPSG:4326")

# Создание примерных данных для участков земель под сельское хозяйство
farm_coords = [(48.3550, 39.2050), (48.3650, 39.2150), (48.3750, 39.2250)]
farm_points = [Point(coord) for coord in farm_coords]
farm_gdf = gpd.GeoDataFrame({'name': ['Участок 1', 'Участок 2', 'Участок 3'], 'geometry': farm_points}, crs="EPSG:4326")

# Шаг 2: Обработка данных
# В данном примере предположим, что данные уже очищены и готовы к использованию.

# Шаг 3: Моделирование
# Простая модель линейного распространения соли от реки к окружающим землям.
def calculate_salinity(point, river_line):
    distance = point.distance(river_line)
    # Предположим, что соленость уменьшается экспоненциально с расстоянием
    salinity = 10 * np.exp(-distance / 1000)  # Примерная формула для демонстрации
    return salinity

farm_gdf['salinity'] = farm_gdf['geometry'].apply(lambda point: calculate_salinity(point, river_line))

# Шаг 4: Визуализация результатов
m = folium.Map(location=[48.3600, 39.2100], zoom_start=13)

# Добавление реки на карту
folium.GeoJson(river_gdf).add_to(m)

# Добавление участков земель с цветовой градацией в зависимости от уровня солености
for _, row in farm_gdf.iterrows():
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=10,
        color='blue',
        fill=True,
        fill_color='blue' if row['salinity'] < 2 else 'yellow' if row['salinity'] < 5 else 'red',  # Цветовая градация
        fill_opacity=0.6,
        popup=f"Участок: {row['name']}, Соленость: {row['salinity']:.2f}"
    ).add_to(m)

# Сохранение карты в файл
m.save("195.html")