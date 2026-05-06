import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 37.7749, 'lon': -122.4194},
    {'lat': 38.8977, 'lon': -77.0365},
    {'lat': 29.7604, 'lon': -95.3698}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Точка').add_to(m)

# Сохранить карту в файл
m.save("279.html")