import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_gdf.unary_union.__geo_interface__, name='Basin').add_to(m)

# Создание списка словарей с координатами наблюдений (предположительно)
observations = [
    {'name': 'Observation 1', 'geometry': wkt.loads('POINT(12.3456 45.6789)')},
    {'name': 'Observation 2', 'geometry': wkt.loads('POINT(13.4567 46.7890)')},
    {'name': 'Observation 3', 'geometry': wkt.loads('POINT(14.5678 47.8901)')}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(observation['geometry'].coords[0], popup=observation['name']).add_to(m)

# Сохранение карты в файл
m.save("94.html")