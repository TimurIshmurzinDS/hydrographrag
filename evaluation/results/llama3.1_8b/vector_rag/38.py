import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с границами бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить границы бассейна на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 77.5678},
    {'lat': 42.9012, 'lon': 78.3456}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("38.html")