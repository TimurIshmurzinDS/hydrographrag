import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с внешними границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(basin_gdf.to_json(), name='basin').add_to(m)

# Создайте список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.2345, 'lon': 76.6543},
    {'lat': 43.3456, 'lon': 76.7654}
]

# Добавьте точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Точка').add_to(m)

# Сохраните карту в файл
m.save("52.html")