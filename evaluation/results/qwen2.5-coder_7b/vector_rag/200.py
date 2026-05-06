import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат наблюдений (если они есть)
coordinates = [
    {'name': 'Observation 1', 'wkt': 'POINT(139.7654 -34.8901)'},
    {'name': 'Observation 2', 'wkt': 'POINT(139.7754 -34.8801)'},
    {'name': 'Observation 3', 'wkt': 'POINT(139.7654 -34.8701)'},
    {'name': 'Observation 4', 'wkt': 'POINT(139.7554 -34.8601)'}
]

# Добавление точек наблюдений на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("200.html")