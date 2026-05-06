import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создайте карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создайте список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 55.7558, 'lon': 37.6173},
    {'lat': 55.7632, 'lon': 37.6234},
    {'lat': 55.7706, 'lon': 37.6295},
    # Добавьте остальные координаты
]

# Создайте карту с маркерами на координатах (WKT)
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Маркер').add_to(m)

# Сохраните карту в файл
m.save("50.html")