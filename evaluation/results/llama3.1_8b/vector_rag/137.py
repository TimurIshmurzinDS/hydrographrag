import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile бассейна рек Или и Каратал
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту с центром в середине бассейна
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список с координатами (WKT) для рек Или и Каратал
river_coords = [
    {'name': 'Или', 'coords': wkt.loads('POLYGON ((48.5 67.2, 49.1 66.8, 49.3 67.4, 48.5 67.2))')},
    {'name': 'Каратал', 'coords': wkt.loads('POLYGON ((47.8 65.9, 48.2 65.3, 48.6 66.1, 47.8 65.9))')}
]

# Добавить реки на карту
for river in river_coords:
    folium.Marker(location=[river['coords'].centroid.y, river['coords'].centroid.x], popup=river['name']).add_to(m)

# Сохранить карту в файл
m.save("137.html")