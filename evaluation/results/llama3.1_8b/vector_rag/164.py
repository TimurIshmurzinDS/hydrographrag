import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с внешними границами бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создайте карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Создайте список словарей для координат (WKT)
wkt_coords = [
    {'name': 'Ili River', 'coords': wkt.loads('SRID=4326;GEOMETRYFROMTEXT("LINESTRING(47.0333 74.3333, 48.6667 75.5)")')},
    {'name': 'Shynzhaly River', 'coords': wkt.loads('SRID=4326;GEOMETRYFROMTEXT("LINESTRING(46.7333 73.8333, 47.3667 74.2)")')}
]

# Добавьте координаты на карту
for coord in wkt_coords:
    folium.Marker(location=coord['coords'].coords[0], popup=coord['name']).add_to(m)

# Сохраните карту в файл
m.save("164.html")