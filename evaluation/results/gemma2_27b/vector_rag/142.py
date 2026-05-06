import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о бассейне реки
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в центре бассейна
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Добавить точку наблюдения (если координаты доступны)
observation_points = [
    {'geometry': {'type': 'Point', 'coordinates': [-122.4194, 37.7749]}, 'properties': {'name': 'Observation Point'}}
]

for point in observation_points:
    folium.Marker(location=[point['geometry']['coordinates'][1], point['geometry']['coordinates'][0]], popup=point['properties']['name']).add_to(m)

# Сохранить карту
m.save("142.html")