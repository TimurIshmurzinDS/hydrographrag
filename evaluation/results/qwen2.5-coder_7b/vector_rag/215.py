import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат WKT для наблюдений в Bayankol village (если они есть)
coordinates = [
    {'name': 'Bayankol village 1', 'wkt': 'POINT(67.4538 43.0923)'},
    {'name': 'Bayankol village 2', 'wkt': 'POINT(67.4538 43.0923)'},
    {'name': 'Bayankol village 3', 'wkt': 'POINT(67.4538 43.0923)'},
    {'name': 'Bayankol village 4', 'wkt': 'POINT(67.4538 43.0923)'},
    {'name': 'Bayankol village 5', 'wkt': 'POINT(67.4538 43.0923)'}
]

# Добавление точек наблюдений на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("215.html")