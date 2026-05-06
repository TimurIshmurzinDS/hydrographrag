import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shape-файла
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн реки Киши Осек',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек наблюдения
observation_points = [
    {'location': [55.123456, 37.654321], 'type': 'Observation'},
    {'location': [55.234567, 38.765432], 'type': 'Observation'},
    {'location': [55.345678, 39.876543], 'type': 'Observation'},
    {'location': [55.456789, 40.987654], 'type': 'Observation'}
]

# Добавление точек наблюдения на карту
for point in observation_points:
    folium.Marker(point['location'], popup=point['type']).add_to(m)

# Сохранение карты в файл
m.save("190.html")