import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту как GeoJson
folium.GeoJson(data=basin_data.to_json(), name='бассейн').add_to(m)

# Создание списка словарей для координат наблюдения (в данном случае hardcoded)
observation_coords = [
    {'lat': 43.1234, 'lon': 77.5678},
]

# Добавление маркеров на карту для наблюдений
for coord in observation_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("11.html")