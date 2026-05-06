import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создайте карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создайте список словарей с координатами (WKT)
wkt_coords = [
    {"lat": 55.7558, "lon": 37.6173},
    {"lat": 55.7634, "lon": 37.6231},
    {"lat": 55.7710, "lon": 37.6289}
]

# Добавьте координаты на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохраните карту в файл
m.save("221.html")