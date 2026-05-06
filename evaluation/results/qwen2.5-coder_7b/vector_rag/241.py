import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=5, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат для реки Талгар и Луны (замените на реальные данные)
coordinates = [
    {"name": "Talgar River", "wkt": "POINT(45.1234 67.5678)"},
    {"name": "Moon", "wkt": "POINT(-23.4567 -12.3456)"}
]

# Преобразование WKT в координаты
points = [wkt.loads(coord["wkt"]) for coord in coordinates]

# Добавление точек на карту
for point, name in zip(points, [coord["name"] for coord in coordinates]):
    folium.Marker([point.y, point.x], popup=name).add_to(m)

# Сохранение карты
m.save("241.html")