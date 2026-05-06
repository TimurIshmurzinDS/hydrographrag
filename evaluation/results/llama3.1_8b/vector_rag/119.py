import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с внешними границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создайте карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создайте список словарей для координат рек
river_coords = [
    {"name": "Byzhy River", "coords": wkt.loads("SRID=4326;POINT(47.1234 30.5678)")},
    {"name": "Tekeli River", "coords": wkt.loads("SRID=4326;POINT(46.9012 29.3456)")},
    {"name": "Shyzhyn River", "coords": wkt.loads("SRID=4326;POINT(47.6789 30.1234)")}
]

# Добавьте координаты рек на карту
for river in river_coords:
    folium.Marker(river["coords"], popup=river["name"]).add_to(m)

# Сохраните карту в файл
m.save("119.html")