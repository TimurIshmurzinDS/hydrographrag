import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными бассейна в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {'lat': 55.123456, 'lon': 36.789012},
    {'lat': 55.234567, 'lon': 37.890123},
    {'lat': 55.345678, 'lon': 38.901234}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("19.html")