import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_crs(epsg=4326).geometry.__geo_interface__, name='basin').add_to(m)

# Создание списка наблюдений в виде словарей
observations = [
    {'lat': 43.123456, 'lon': 76.789012, 'type': 'Observation'},
    {'lat': 43.123456, 'lon': 76.789012, 'type': 'Observation'},
    {'lat': 43.123456, 'lon': 76.789012, 'type': 'Observation'},
    {'lat': 43.123456, 'lon': 76.789012, 'type': 'Observation'}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker([observation['lat'], observation['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("24.html")