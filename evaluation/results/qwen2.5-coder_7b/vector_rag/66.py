import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о границах ручья
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid границы ручья
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка координат оборудования (пример)
equipment_coords = [
    {'name': 'Equipment1', 'wkt': 'POINT(43.5678 39.1234)'},
    {'name': 'Equipment2', 'wkt': 'POINT(43.5700 39.1250)'},
    {'name': 'Equipment3', 'wkt': 'POINT(43.5690 39.1240)'}
]

# Добавление маркеров оборудования на карту
for equipment in equipment_coords:
    point = wkt.loads(equipment['wkt'])
    folium.Marker([point.y, point.x], popup=equipment['name']).add_to(m)

# Сохранение карты в файл
m.save("66.html")