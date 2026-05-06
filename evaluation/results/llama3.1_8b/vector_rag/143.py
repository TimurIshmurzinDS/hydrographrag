import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами (WKT) для рек Каратал и Коктал
river_coords = [
    {'name': 'Karatal River', 'coords': wkt.loads('POLYGON ((48.678 76.923, 48.678 77.123, 47.878 77.123, 47.878 76.923, 48.678 76.923))')},
    {'name': 'Koktal River', 'coords': wkt.loads('POLYGON ((49.478 78.123, 49.478 79.323, 48.678 79.323, 48.678 78.123, 49.478 78.123))')}
]

# Добавить реки на карту
for river in river_coords:
    folium.Polygon(river['coords'].exterior.coords[:], color='blue', fill_color='lightblue').add_to(m)

# Сохранить карту в файл
m.save("143.html")