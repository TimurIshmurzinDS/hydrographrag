import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создайте карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создайте список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 79.5678},
    {'lat': 42.9012, 'lon': 78.3456}
]

# Добавьте точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранитe карту в файле с именем '129.html'
m.save("129.html")