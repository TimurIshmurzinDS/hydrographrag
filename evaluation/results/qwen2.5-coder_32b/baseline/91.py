import osmnx as ox
import geopandas as gpd
import folium

# Загрузка данных о водных объектах в пределах некоторого радиуса от точки, принадлежащей реке Уржар.
# Координаты точки на реке Уржар (примерные): широта 51.3806, долгота 47.2944
center_point = (51.3806, 47.2944)
radius = 10000  # радиус в метрах

# Загрузка данных о водных объектах
tags = {'waterway': ['stream', 'river']}
gdf = ox.geometries_from_point(center_point, tags=tags, dist=radius)

# Фильтрация притоков реки Уржар (предположим, что они имеют тег 'name' с названием притока)
tributaries = gdf[gdf['name'].str.contains('Уржар', na=False)]

# Извлечение координат притоков
coordinates = [(point.y, point.x) for point in tributaries.geometry.centroid]

# Создание интерактивной карты с помощью folium
m = folium.Map(location=center_point, zoom_start=12)

# Добавление маркеров на карту для каждого притока
for coord in coordinates:
    folium.Marker(coord).add_to(m)

# Сохранение карты в файл
m.save("91.html")

# Вывод координат притоков
print("Координаты притоков реки Уржар:")
for i, coord in enumerate(coordinates):
    print(f"Приток {i+1}: Широта = {coord[0]}, Долгота = {coord[1]}")