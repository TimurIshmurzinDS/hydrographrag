import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна Urzhar River
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в геометрии бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат наблюдений (WKT)
coordinates = [
    {'name': 'Observation_2264', 'wkt': 'POINT(51.3456 45.7890)'},
    {'name': 'Observation_2247', 'wkt': 'POINT(52.3456 46.7890)'},
    {'name': 'Observation_2265', 'wkt': 'POINT(53.3456 47.7890)'}
]

# Преобразование координат в GeoPoints
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("209.html")