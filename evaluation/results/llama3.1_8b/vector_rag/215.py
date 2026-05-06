import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 52.5, 'lon': 106.7},
    {'lat': 53.2, 'lon': 107.1},
    {'lat': 52.8, 'lon': 106.9},
    {'lat': 53.0, 'lon': 107.0},
    {'lat': 52.6, 'lon': 106.8}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("215.html")