import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с географическими границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление географических границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Добавление речных систем на карту (если есть координаты)
river_coords = [
    {'name': 'Shynzhaly River', 'wkt': 'LINESTRING(45.123 78.901, 46.234 79.012)'},
    {'name': 'Shilik River', 'wkt': 'LINESTRING(47.345 80.123, 48.456 81.234)'}
]

for river in river_coords:
    geom = wkt.loads(river['wkt'])
    folium.GeoJson({'type': 'Feature', 'geometry': geom}, style_function=lambda x: {
        'color': 'blue',
        'weight': 2
    }).add_to(m)

# Добавление точек с высотой водного уровня (если есть)
water_level_coords = [
    {'name': 'Water Level 1', 'wkt': 'POINT(45.123 78.901)'},
    {'name': 'Water Level 2', 'wkt': 'POINT(46.234 79.012)'}
]

for point in water_level_coords:
    geom = wkt.loads(point['wkt'])
    folium.CircleMarker(location=[geom.y, geom.x], radius=5, color='red', fill=True, fill_color='red').add_to(m)

# Сохранение карты
m.save("161.html")