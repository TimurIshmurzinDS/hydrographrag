import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре масса бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат датчиков (WKT)
sensor_coordinates = [
    {'name': 'Sensor_1', 'wkt': 'POINT(37.6543 55.1234)'},
    {'name': 'Sensor_2', 'wkt': 'POINT(37.7890 55.2345)'}
]

# Добавление датчиков на карту
for sensor in sensor_coordinates:
    point = wkt.loads(sensor['wkt'])
    folium.Marker([point.y, point.x], popup=sensor['name']).add_to(m)

# Сохранение карты в файл
m.save("140.html")