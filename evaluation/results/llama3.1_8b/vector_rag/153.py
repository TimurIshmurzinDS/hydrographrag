import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile бассейна в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_gdf.unary_union.__geo_interface__, name='basin').add_to(m)

# Создание списка наблюдений ниже устья реки Сарысай
observations = [
    {'type': 'Observation', 'geometry': wkt.loads('POINT(48.6784 69.3245)')},
    {'type': 'Observation', 'geometry': wkt.loads('POINT(48.6792 69.3251)')},
    {'type': 'Observation', 'geometry': wkt.loads('POINT(48.6800 69.3256)')},
    {'type': 'Observation', 'geometry': wkt.loads('POINT(48.6808 69.3261)')}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(observation['geometry'].coords[0], popup='Наблюдение').add_to(m)

# Сохранение карты в файл
m.save("153.html")