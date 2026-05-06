import folium
from shapely.geometry import Point, Polygon
import geopandas as gpd

# Шаг 1: Сбор данных о координатах рек
rivers = {
    "Улькен Алматы": (42.8603, 75.9254),
    "Емель": (42.8583, 75.9217),
    "Тентек": (42.8563, 75.9180)
}

# Шаг 2: Определение региона
# Для примера создадим простой полигон, который будет представлять регион.
# В реальном сценарии можно использовать данные из GeoJSON или других географических форматов.

# Пример полигона (координаты должны быть заменены на реальные границы региона)
region_polygon = Polygon([
    (75.91, 42.86),
    (75.93, 42.86),
    (75.93, 42.85),
    (75.91, 42.85)
])

# Шаг 3: Анализ и сравнение
rivers_in_region = []
for river_name, coordinates in rivers.items():
    point = Point(coordinates[1], coordinates[0])
    if region_polygon.contains(point):
        rivers_in_region.append(river_name)

print(f"Реки в одном регионе: {rivers_in_region}")

# Шаг 4: Визуализация
m = folium.Map(location=[42.8593, 75.9234], zoom_start=14)  # Центральная точка карты

# Добавление полигона региона на карту
folium.GeoJson(region_polygon).add_to(m)

# Добавление маркеров для рек
for river_name, coordinates in rivers.items():
    folium.Marker(
        location=[coordinates[0], coordinates[1]],
        popup=river_name,
        icon=folium.Icon(color='blue' if river_name in rivers_in_region else 'red')
    ).add_to(m)

# Сохранение карты
m.save("105.html")