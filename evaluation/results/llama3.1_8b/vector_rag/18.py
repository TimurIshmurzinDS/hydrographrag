import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с зеленой заливкой
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений в деревне Bayankol
observations = [
    {'location': [48.1234, 87.5678], 'type': 'Observation'},
    {'location': [48.2345, 87.6789], 'type': 'Observation'},
    {'location': [48.3456, 87.7890], 'type': 'Observation'},
    {'location': [48.4567, 87.8901], 'type': 'Observation'}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(observation['location'], popup=observation['type']).add_to(m)

# Сохранение карты в файл
m.save("18.html")