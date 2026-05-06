import geopandas as gpd
import folium
from shapely import wkt

# Загрузка и подготовка данных
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат (если они есть)
coordinates = [
    {'name': 'Point1', 'wkt': 'POINT(10 20)'},
    {'name': 'Point2', 'wkt': 'POINT(30 40)'}
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("285.html")