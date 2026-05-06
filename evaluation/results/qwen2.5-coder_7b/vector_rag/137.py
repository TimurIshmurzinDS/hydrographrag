import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Определение координат центра масс для каждого бассейна
centroids = basin_data.geometry.centroid

# Инициализация карты с центром в каждом бассейне
m = folium.Map(location=[centroids.y.mean(), centroids.x.mean()], zoom_start=6, tiles='CartoDB positron')

# Добавление бассейнов на карту
folium.GeoJson(basin_data.geometry, 
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если в контексте есть координаты датчиков (WKT), добавим их на карту
sensor_coordinates = [
    {"name": "Датчик 1", "wkt": "POINT(43.6578 49.8523)"},
    {"name": "Датчик 2", "wkt": "POINT(44.1234 49.0123)"}
]

for sensor in sensor_coordinates:
    point = wkt.loads(sensor["wkt"])
    folium.Marker([point.y, point.x], popup=sensor["name"], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("137.html")