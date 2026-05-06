import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре масс бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат точек на русле реки Шилик (замените на реальные данные)
river_points = [
    {"lat": 51.48, "lon": 76.32},
    {"lat": 51.49, "lon": 76.33},
    {"lat": 51.50, "lon": 76.34},
    # Добавьте больше точек по необходимости
]

# Вычисление извилистости на основе координат точек
def calculate_meandering_factor(points):
    total_length = 0
    for i in range(len(points) - 1):
        total_length += ((points[i+1]['lon'] - points[i]['lon'])**2 + (points[i+1]['lat'] - points[i]['lat'])**2)**0.5
    return total_length / len(points)

meandering_factor = calculate_meandering_factor(river_points)
print(f"Извилистость реки Шилик: {meandering_factor}")

# Генерация случайного числа на основе извилистости
import random
random_number = random.uniform(0, meandering_factor)
print(f"Случайное число на основе извилистости: {random_number}")

# Сохранение карты
m.save("254.html")