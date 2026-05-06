import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в centroid shapefile и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о датчиках уровня (если доступны)
sensor_data = [
    {'name': 'Sensor1', 'wkt': 'POINT(37.5648 45.0395)', 'water_level': 120},
    {'name': 'Sensor2', 'wkt': 'POINT(37.5748 45.0495)', 'water_level': 130}
]

# Добавление датчиков уровня на карту
for sensor in sensor_data:
    point = wkt.loads(sensor['wkt'])
    folium.Marker([point.y, point.x], popup=f"{sensor['name']}: Уровень воды {sensor['water_level']} см").add_to(m)

# Сохранение финальной карты
m.save("72.html")