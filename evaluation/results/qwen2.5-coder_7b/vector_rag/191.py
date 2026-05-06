import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат для наблюдений (если они доступны)
coordinates = [
    {'name': 'Observation_2264', 'geometry': wkt.loads('POINT(37.12345 45.67890)')},
    {'name': 'Observation_2247', 'geometry': wkt.loads('POINT(37.23456 45.78901)')},
    {'name': 'Observation_2278', 'geometry': wkt.loads('POINT(37.34567 45.89012)')},
    {'name': 'Observation_2248', 'geometry': wkt.loads('POINT(37.45678 45.90123)')}
]

# Добавление точек наблюдений на карту
for coord in coordinates:
    folium.Marker([coord['geometry'].y, coord['geometry'].x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("191.html")