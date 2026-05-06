import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import numpy as np

# Шаг 1: Сбор данных
# Предположим, что у нас есть GeoJSON файл с топографией реки Тентек и ее притоков.
file_path = 'tentek_river_network.geojson'
river_network = gpd.read_file(file_path)

# Шаг 2: Подготовка данных
# Преобразуем данные в формат GeoDataFrame, если это еще не сделано.
if not isinstance(river_network, gpd.GeoDataFrame):
    river_network = gpd.GeoDataFrame(river_network)

# Шаг 3: Определение параметров орбиты спутника
# Задаем начальные координаты и другие параметры орбиты.
initial_latitude = 51.807249  # Примерные координаты реки Тентек
initial_longitude = 39.617778
orbit_altitude = 500  # Высота орбиты в км

# Шаг 4: Моделирование орбиты спутника
# Для простоты моделируем круговую орбиту вокруг средней точки реки.
center_point = river_network.geometry.centroid.iloc[0]
center_latitude, center_longitude = center_point.y, center_point.x

# Генерация точек орбиты (примерная модель)
num_points = 100
angles = np.linspace(0, 2 * np.pi, num_points)
orbit_radius = orbit_altitude / 6371  # Преобразуем радиус в градусы для сферической модели

orbit_latitudes = center_latitude + (orbit_radius * np.sin(angles))
orbit_longitudes = center_longitude + (orbit_radius * np.cos(angles))

# Создаем линию орбиты
orbit_points = [Point(lon, lat) for lon, lat in zip(orbit_longitudes, orbit_latitudes)]
orbit_line = LineString(orbit_points)

# Шаг 5: Визуализация результатов
# Создание карты с использованием folium
m = folium.Map(location=[center_latitude, center_longitude], zoom_start=10)

# Добавление топографии реки на карту
folium.GeoJson(river_network).add_to(m)

# Добавление орбиты спутника на карту
folium.PolyLine(locations=[[p.y, p.x] for p in orbit_points], color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("250.html")