import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'name': 'Byzhy River', 'coords': wkt.loads('POINT(48.123 77.456)')},
    {'name': 'Urzhar River', 'coords': wkt.loads('POINT(49.789 80.321)')},
    {'name': 'Shyzhyn River', 'coords': wkt.loads('POINT(47.654 76.987)')},
    {'name': 'Uzyn Kargaly River', 'coords': wkt.loads('POINT(48.901 79.123)')},
    {'name': 'Shynzhaly River', 'coords': wkt.loads('POINT(49.321 77.654)')}
]

# Добавить координаты на карту
for coord in wkt_coords:
    folium.Marker(location=coord['coords'].coords[0], popup=coord['name']).add_to(m)

# Сохранить карту в файл
m.save("204.html")