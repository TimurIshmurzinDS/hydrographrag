import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя "CartoDB positron"
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_json(), name='бассейн').add_to(m)

# Создание списка точек наблюдения (в данном случае hardcoded)
points = [
    {'location': [48.1234, 87.5678], 'name': 'Баянкольская деревня'},
    {'location': [48.2345, 88.9012], 'name': 'Деревня Баянколь'},
    {'location': [47.6789, 86.5432], 'name': 'Баянкольская деревня'}
]

# Добавление точек наблюдения на карту
for point in points:
    folium.Marker(location=point['location'], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("257.html")