import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты folium
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты деревни Бутак в формате WKT
coordinates = [
    {"name": "Butak village", "wkt": "POINT(37.618423 55.755814)"},  # Примерные координаты Москвы, заменить на реальные
    {"name": "Butak village", "wkt": "POINT(37.618423 55.755814)"},
    {"name": "Butak village", "wkt": "POINT(37.618423 55.755814)"},
    {"name": "Butak village", "wkt": "POINT(37.618423 55.755814)"}
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("262.html")