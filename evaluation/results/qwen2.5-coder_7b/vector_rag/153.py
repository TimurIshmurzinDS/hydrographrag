import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна Sarykan River
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в бассейне
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат рек (если они доступны)
river_coords = [
    {'name': 'River A', 'wkt': 'POINT(37.123456 40.987654)'},
    {'name': 'River B', 'wkt': 'POINT(37.567890 41.123456)'},
    {'name': 'River C', 'wkt': 'POINT(38.123456 40.567890)'}
]

# Добавление рек на карту
for river in river_coords:
    point = wkt.loads(river['wkt'])
    folium.Marker([point.y, point.x], popup=river['name']).add_to(m)

# Сохранение карты
m.save("153.html")