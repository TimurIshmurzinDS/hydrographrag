import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.unary_union.__geo_interface__, name='basin').add_to(m)

# Создать список словарей с координатами (WKT) для реки Сарыкан
river_coords = [
    {'type': 'Feature', 'geometry': wkt.loads('POLYGON ((...))'), 'properties': {}},
]

# Добавить точки на карту
for coord in river_coords:
    folium.Marker(location=coord['geometry'].coords[0], popup='Река Сарыкан').add_to(m)

# Сохранить карту в файл
m.save("46.html")