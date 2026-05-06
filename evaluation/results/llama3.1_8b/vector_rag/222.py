import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными бассейна в формате EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить данные бассейна на карту в виде GeoJson с зеленой заливкой
folium.GeoJson(data=basin_data.to_json(), name='Basin').add_to(m)

# Создать список словарей для координат WKT (в данном случае hardcoded)
wkt_coords = [
    {'lat': 43.1234, 'lon': 77.5678},
    {'lat': 42.9012, 'lon': 78.3456}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл html
m.save("222.html")