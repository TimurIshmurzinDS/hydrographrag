import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.unary_union.__geo_interface__, name='basin').add_to(m)

# Создание списка словарей для наблюдений с координатами WKT
observations = [
    {'name': 'Observation 1', 'wkt': wkt.loads('POINT(55.1234 37.5678)')},
    {'name': 'Observation 2', 'wkt': wkt.loads('POINT(55.1234 37.5678)')},
    {'name': 'Observation 3', 'wkt': wkt.loads('POINT(55.1234 37.5678)')},
    {'name': 'Observation 4', 'wkt': wkt.loads('POINT(55.1234 37.5678)')}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(location=observation['wkt'].coords[0], popup=observation['name']).add_to(m)

# Сохранение карты в файл
m.save("74.html")