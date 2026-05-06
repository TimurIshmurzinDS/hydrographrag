import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты наблюдений (WKT)
observations = [
    {'name': 'Observation 1', 'geometry': wkt.loads('POINT(139.7654 -34.8901)')},
    {'name': 'Observation 2', 'geometry': wkt.loads('POINT(139.7655 -34.8902)')},
    {'name': 'Observation 3', 'geometry': wkt.loads('POINT(139.7656 -34.8903)')},
    {'name': 'Observation 4', 'geometry': wkt.loads('POINT(139.7657 -34.8904)')}
]

# Добавление наблюдений на карту
for obs in observations:
    folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# Сохранение карты в файл
m.save("190.html")