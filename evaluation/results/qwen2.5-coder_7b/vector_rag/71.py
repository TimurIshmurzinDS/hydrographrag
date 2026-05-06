import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Byzhy River из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid области ручья
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление области ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты сенсоров (пример)
sensors = [
    {'name': 'Sensor1', 'wkt': 'POINT(37.5648 49.8756)', 'status': 'active'},
    {'name': 'Sensor2', 'wkt': 'POINT(37.5700 49.8800)', 'status': 'inactive'},
    {'name': 'Sensor3', 'wkt': 'POINT(37.5750 49.8850)', 'status': 'active'}
]

# Добавление сенсоров на карту
for sensor in sensors:
    point = wkt.loads(sensor['wkt'])
    if sensor['status'] == 'active':
        folium.Marker([point.y, point.x], popup=sensor['name'], icon=folium.Icon(color='green')).add_to(m)
    else:
        folium.Marker([point.y, point.x], popup=sensor['name'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("71.html")