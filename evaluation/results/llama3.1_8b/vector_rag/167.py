import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузить shapefile с данными бассейна в формате EPSG:4326
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# 2. Создать карту Folium с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# 3. Создать список координат рек в формате WKT
river_coords = [
    {'name': 'Tentek River', 'coords': wkt.loads('POLYGON ((...))')},
    {'name': 'Tekes River', 'coords': wkt.loads('POLYGON ((...))')}
]

# 4. Рассчитать общую протяженность речной сети
total_length = 0
for river in river_coords:
    total_length += river['coords'].length

# 5. Добавить на карту координаты рек и их длину
for river in river_coords:
    folium.Marker(location=river['coords'].centroid.coords[0], popup=f'{river["name"]}: {river["coords"].length} м').add_to(m)

# 6. Сохранить карту в файл
m.save("167.html")