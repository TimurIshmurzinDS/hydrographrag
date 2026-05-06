import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coords = [
    {'lat': 55.0, 'lon': 37.0},
    {'lat': 56.0, 'lon': 38.0},
    {'lat': 57.0, 'lon': 39.0},
    {'lat': 58.0, 'lon': 40.0},
    {'lat': 59.0, 'lon': 41.0}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Золотая находка').add_to(m)

# Сохранение карты в файл
m.save("274.html")