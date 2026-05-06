import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с бассейнами
basins_gdf = gpd.read_file(r"data/basin_data.shp")
basins_gdf.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна
m = folium.Map(location=basins_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basins_gdf.to_json(), name='bassins').add_to(m)

# Создание списка координат рек Тентек и Быж
river_coords = [
    {'name': 'Tentek River', 'coords': wkt.loads('POINT(55.123 37.456)')},
    {'name': 'Byzhy River', 'coords': wkt.loads('POINT(56.789 38.012)')}
]

# Добавление рек на карту
for river in river_coords:
    folium.Marker(location=river['coords'].coords[0], popup=river['name']).add_to(m)

# Сохранение карты в файл
m.save("98.html")