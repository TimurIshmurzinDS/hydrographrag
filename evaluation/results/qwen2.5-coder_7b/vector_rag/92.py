import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты устья реки Дос и начала реки Емель (примерные значения)
coordinates = [
    {"name": "Устье реки Дос", "wkt": "POINT(37.12345 56.78901)"},
    {"name": "Начало реки Емель", "wkt": "POINT(38.23456 57.89012)"}
]

# Преобразование WKT в координаты
points = [wkt.loads(coord["wkt"]) for coord in coordinates]

# Вычисление расстояния между двумя точками
from geopy.distance import geodesic

distance = geodesic(points[0], points[1]).kilometers
print(f"Расстояние между устьем реки Дос и началом реки Емель: {distance:.2f} километров")

# Добавление маркеров на карту
for coord in coordinates:
    folium.Marker([coord["wkt"].y, coord["wkt"].x], popup=coord["name"]).add_to(m)

# Сохранение карты
m.save("92.html")