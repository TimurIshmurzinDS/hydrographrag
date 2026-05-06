# Библиотеки для работы с геоданными
import geopandas as gpd
from shapely.geometry import Point

# Библиотека для визуализации карт
import folium

# Загрузка данных о Луне (в формате GeoJSON)
moon_data = gpd.read_file("moon_surface.geojson")

# Координаты реки Киши Осек (примерные)
river_coords = Point(10, 20)

# Создание карты
m = folium.Map(location=[0, 0], zoom_start=3)

# Визуализация данных о Луне
folium.GeoJson("moon_surface.geojson").add_to(m)

# Пометить координаты реки
folium.Marker(location=[river_coords.y, river_coords.x]).add_to(m)

# Сохранение карты
m.save("269.html")