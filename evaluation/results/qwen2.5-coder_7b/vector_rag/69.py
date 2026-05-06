import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid shapefile и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат датчиков (WKT) для Koktal River и Aksu River
sensor_points = [
    {'name': 'Koktal River Sensor 1', 'wkt': 'POINT(45.1234 78.9012)', 'color': 'red'},
    {'name': 'Koktal River Sensor 2', 'wkt': 'POINT(46.1234 79.9012)', 'color': 'blue'},
    {'name': 'Aksu River Sensor 1', 'wkt': 'POINT(50.1234 80.9012)', 'color': 'green'}
]

# Добавление датчиков на карту
for sensor in sensor_points:
    point = wkt.loads(sensor['wkt'])
    folium.Marker([point.y, point.x], popup=sensor['name'], icon=folium.Icon(color=sensor['color'])).add_to(m)

# Сохранение финальной карты
m.save("69.html")