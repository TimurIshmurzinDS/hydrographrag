import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна и заданием тайлов
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат наблюдений в Байанкольском селе (WKT)
observations = [
    {'name': 'Observation 1', 'geometry': wkt.loads('POINT(74.5678 43.2109)')},
    {'name': 'Observation 2', 'geometry': wkt.loads('POINT(74.5700 43.2120)')},
    {'name': 'Observation 3', 'geometry': wkt.loads('POINT(74.5695 43.2115)')}
]

# Добавление наблюдений на карту
for obs in observations:
    folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# Сохранение карты в файл
m.save("151.html")