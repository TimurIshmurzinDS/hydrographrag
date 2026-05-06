import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с данными бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создайте карту Folium с центром в координатах центра shapefile и параметрами tiles='CartoDB positron'
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту с помощью GeoJson
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создайте список словарей для координат (WKT)
wkt_coords = [
    {'lat': 55.123, 'lon': 37.456},
    {'lat': 55.789, 'lon': 38.901}
]

# Добавьте точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохраните карту в файл с именем "27.html"
m.save("27.html")