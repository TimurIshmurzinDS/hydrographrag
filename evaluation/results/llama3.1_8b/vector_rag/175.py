import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с бассейном
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Создайте карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=[basin_gdf.centroid.y, basin_gdf.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту с помощью folium.GeoJson
folium.GeoJson(data=basin_gdf.to_json(), name='bassain').add_to(m)

# Создайте список словарей для координат (WKT)
wkt_coords = [
    {'lat': 55.123, 'lon': 37.456},
    {'lat': 55.789, 'lon': 38.901},
    {'lat': 56.321, 'lon': 39.654}
]

# Добавьте координаты на карту с помощью folium.Marker
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']]).add_to(m)

# Сохраните карту в файл
m.save("175.html")