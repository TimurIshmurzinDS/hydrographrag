import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Если в контексте есть координаты (WKT), создаем список словарей с координатами
coordinates = [
    {'name': 'Ili River', 'wkt': 'POINT(74.5678 43.1234)'},
    {'name': 'Shynzhaly River', 'wkt': 'POINT(75.6789 44.2345)'}
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("164.html")