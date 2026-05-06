import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты точек наблюдений в формате WKT
observations_wkt = [
    "POINT(69.12345 41.12345)",
    "POINT(69.12345 41.12346)"
]

# Преобразование координат из WKT в объекты Shapely
observations = [wkt.loads(obs) for obs in observations_wkt]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker([obs.y, obs.x], popup="Observation Point").add_to(m)

# Генерация случайных чисел на основе извилистости русла реки Шилик
import random

# Предположим, что извилистость определяется как длина линии (для примера)
winding_length = 15.0  # Примерная длина русловой линии в км

# Генерация случайного числа на основе длины линии
random_number = random.uniform(0, winding_length)

print(f"Случайное число на основе извилистости русла реки Шилик: {random_number}")

# Сохранение карты в файл
m.save("254.html")