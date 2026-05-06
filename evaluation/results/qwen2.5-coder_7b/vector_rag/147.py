import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Определение координат датчиков (пример)
sensor_coords = [
    {'name': 'Датчик 1', 'wkt': 'POINT(75.1234 40.5678)'},
    {'name': 'Датчик 2', 'wkt': 'POINT(75.9876 41.2345)'},
    {'name': 'Датчик 3', 'wkt': 'POINT(76.3456 40.9876)'}
]

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Добавление датчиков на карту
for sensor in sensor_coords:
    point = wkt.loads(sensor['wkt'])
    folium.Marker([point.y, point.x], popup=sensor['name']).add_to(m)

# Сохранение карты
m.save("147.html")