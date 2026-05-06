import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile в GeoPandas DataFrame и преобразуйте его в систему координат 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту Folium с центром в середине области
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте область на карту
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# Создайте список словарей для координат (WKT)
wkt_coords = [
    {'type': 'Point', 'coordinates': wkt.loads('SRID=4326;POINT(84.1234 42.5678)')},
    {'type': 'Point', 'coordinates': wkt.loads('SRID=4326;POINT(85.9012 43.1111)')}
]

# Добавьте точки на карту
for coord in wkt_coords:
    folium.Marker(location=coord['coordinates'], popup='Координаты').add_to(m)

# Сохраните карту в файл
m.save("85.html")