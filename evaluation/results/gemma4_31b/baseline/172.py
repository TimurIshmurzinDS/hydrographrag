import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import folium

def calculate_drainage_density(basin_poly, river_lines):
    """
    Вычисляет плотность дренажной сети.
    D_d = Total Length / Total Area
    """
    # Расчет общей длины всех рек (в метрах, если координаты в проекции)
    total_length = river_lines.length.sum()
    
    # Расчет площади бассейна
    total_area = basin_poly.area
    
    density = total_length / total_area if total_area != 0 else 0
    return density, total_length, total_area

# 1. Симуляция геоданных для бассейна реки Текес 
# (Так как реальные shape-файлы отсутствуют, создаем синтетические данные, 
# имитирующие топологию бассейна в районе Казахстана)

# Координаты центральной части бассейна Текес (примерно)
center_lat, center_lon = 49.5, 81.0

# Создаем полигон бассейна (упрощенно)
basin_coords = [
    (center_lon - 1, center_lat - 1),
    (center_lon + 1, center_lat - 1),
    (center_lon + 1, center_lat + 1),
    (center_lon - 1, center_lat + 1),
    (center_lon - 1, center_lat - 1)
]
basin_geom = Polygon(basin_coords)
basin_gdf = gpd.GeoDataFrame([{'geometry': basin_geom}], crs="EPSG:4326")

# Создаем синтетическую дренажную сеть (основная река и притоки)
# Основное русло
main_river = LineString([
    (center_lon - 0.8, center_lat - 0.5),
    (center_lon - 0.2, center_lat),
    (center_lon + 0.5, center_lat + 0.2)
])

# Притоки (топологически привязанные к основной реке)
tributaries = [
    LineString([(center_lon - 0.6, center_lat - 0.8), (center_lon - 0.5, center_lat - 0.5)]),
    LineString([(center_lon - 0.3, center_lat - 0.7), (center_lon - 0.2, center_lat - 0.3)]),
    LineString([(center_lon + 0.1, center_lat + 0.5), (center_lon - 0.1, center_lat)]),
    LineString([(center_lon + 0.4, center_lat + 0.6), (center_lon + 0.3, center_lat + 0.2)]),
]

rivers_gdf = gpd.GeoDataFrame({'geometry': [main_river] + tributaries}, crs="EPSG:4326")

# 2. Перевод в метрическую систему (UTM) для корректного расчета длин и площадей
# Используем зону 43N (подходит для данного региона)
basin_projected = basin_gdf.to_crs(epsg=32643)
rivers_projected = rivers_gdf.to_crs(epsg=32643)

# 3. Расчет плотности
density, length, area = calculate_drainage_density(
    basin_projected.geometry.iloc[0], 
    rivers_projected.geometry
)

print(f"Общая длина сети: {length/1000:.2f} км")
print(f"Площадь бассейна: {area/1e6:.2f} кв. км")
print(f"Плотность дренажной сети: {density:.4f} км/кв. км")

# 4. Визуализация с помощью folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {'fillColor': 'lightblue', 'color': 'blue', 'weight': 2, 'fillOpacity': 0.3},
    name="Бассейн р. Текес"
).add_to(m)

# Добавление речной сети на карту
folium.GeoJson(
    rivers_gdf, 
    style_function=lambda x: {'color': 'blue', 'weight': 3},
    name="Дренажная сеть"
).add_to(m)

# Добавление текстовой метки с результатом
folium.Marker(
    [center_lat, center_lon], 
    popup=f"Плотность сети: {density:.4f} км/км²",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

folium.LayerControl().add_to(m)

# Сохранение карты
m.save("172.html")