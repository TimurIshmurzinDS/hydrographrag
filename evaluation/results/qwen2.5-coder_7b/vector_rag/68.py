import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат для датчиков (если они есть)
sensor_coordinates = [
    {"name": "Sensor 1", "wkt": "POINT(37.5648 55.7558)"},
    {"name": "Sensor 2", "wkt": "POINT(37.5650 55.7560)"},
    {"name": "Sensor 3", "wkt": "POINT(37.5652 55.7562)"}
]

# Преобразование WKT в объекты Shapely
sensor_points = [wkt.loads(coord["wkt"]) for coord in sensor_coordinates]

# Добавление датчиков на карту
for point, name in zip(sensor_points, [coord["name"] for coord in sensor_coordinates]):
    folium.Marker([point.y, point.x], popup=name).add_to(m)

# Сохранение карты в файл
m.save("68.html")