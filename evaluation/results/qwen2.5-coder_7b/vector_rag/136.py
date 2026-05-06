import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами региона и преобразование в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid региона и тайлами 'CartoDB positron'
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ регионов на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат WKT для датчиков уровня воды (замените на реальные данные)
sensor_data = [
    {'name': 'Датчик 1', 'wkt': 'POINT(37.422 -122.084)', 'water_level_value': 50, 'water_quality_class': 'A'},
    {'name': 'Датчик 2', 'wkt': 'POINT(37.425 -122.086)', 'water_level_value': 60, 'water_quality_class': 'B'}
]

# Преобразование WKT в координаты и добавление маркеров на карту
for sensor in sensor_data:
    point = wkt.loads(sensor['wkt'])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Датчик: {sensor['name']}<br>Уровень воды: {sensor['water_level_value']} см<br>Класс качества воды: {sensor['water_quality_class']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение финальной карты
m.save("136.html")