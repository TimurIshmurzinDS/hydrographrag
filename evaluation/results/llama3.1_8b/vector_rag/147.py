import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек наблюдения Butak village
observation_points = [
    {'location': [40.1234, 69.5678], 'name': 'Butak village'},
    {'location': [40.2345, 70.0123], 'name': 'Butak village'},
    {'location': [40.3456, 70.4567], 'name': 'Butak village'},
    {'location': [40.4567, 70.8901], 'name': 'Butak village'}
]

# Добавление точек наблюдения на карту
for point in observation_points:
    folium.Marker(point['location'], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("147.html")