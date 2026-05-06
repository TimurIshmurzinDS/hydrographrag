import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с внешними границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_gdf.unary_union.__geo_interface__, name='basin').add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 74.5678},
    {'lat': 42.9012, 'lon': 75.3456}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("159.html")