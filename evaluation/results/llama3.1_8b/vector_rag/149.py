import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с внешними границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(basin_gdf.to_json(), name='basin').add_to(m)

# Создайте список словарей для визуализации наблюдений с координатами WKT
observations = [
    {'name': 'Observation_0', 'geometry': wkt.loads('POINT(55.123 37.456)')},
    {'name': 'Observation_1', 'geometry': wkt.loads('POINT(56.789 38.901)')},
    {'name': 'Observation_2264', 'geometry': wkt.loads('POINT(54.321 36.654)')}
]

# Добавьте наблюдения на карту
for observation in observations:
    folium.Marker(observation['geometry'].coords[0], popup=observation['name']).add_to(m)

# Сохраните карту в файл
m.save("149.html")