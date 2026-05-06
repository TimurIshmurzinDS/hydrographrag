import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат WKT для наблюдений (если они есть)
coordinates = [
    {'name': 'Bayankol village 1', 'wkt': 'POINT(67.543 43.214)'},
    {'name': 'Bayankol village 2', 'wkt': 'POINT(68.123 43.567)'},
    {'name': 'Bayankol village 3', 'wkt': 'POINT(67.901 43.890)'},
    {'name': 'Bayankol village 4', 'wkt': 'POINT(67.234 43.654)'},
    {'name': 'Bayankol village 5', 'wkt': 'POINT(67.789 43.123)'}
]

# Добавление точек наблюдений на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("223.html")