import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание координат для притоков (примерные значения)
prongs = [
    {"name": "Tekes River", "geometry": wkt.loads("LINESTRING(10 5, 15 10)")},
    {"name": "Osek River", "geometry": wkt.loads("LINESTRING(20 5, 25 10)")},
    {"name": "0.2 km above the confluence with Osek River", "geometry": wkt.loads("LINESTRING(23 7, 28 12)")}
]

# Добавление притоков на карту
for prong in prongs:
    folium.GeoJson(prong["geometry"].wkt, style_function=lambda x: {'color': 'red', 'weight': 2}).add_to(m)

# Сохранение карты в файл
m.save("242.html")