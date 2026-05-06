import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о местоположении датчиков и их значениях уровня воды
sensor_data = [
    {'name': 'Датчик 1', 'wkt': 'POINT(37.5648 55.903)', 'water_level_value': 2.5, 'date_water_level_value': '2023-04-01'},
    {'name': 'Датчик 2', 'wkt': 'POINT(37.5648 55.903)', 'water_level_value': None, 'date_water_level_value': '2023-04-02'},
    {'name': 'Датчик 3', 'wkt': 'POINT(37.5648 55.903)', 'water_level_value': 3.0, 'date_water_level_value': '2023-04-03'}
]

# Добавление датчиков на карту
for sensor in sensor_data:
    point = wkt.loads(sensor['wkt'])
    folium.Marker([point.y, point.x], popup=f"{sensor['name']}: {sensor['water_level_value']} м", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("149.html")