import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных наблюдений (WKT)
observations = [
    {'date': '2019-01-01', 'wkt': 'POINT(37.5648 55.7558)'},
    {'date': '2020-01-01', 'wkt': 'POINT(37.5648 55.7558)'},
    {'date': '2021-01-01', 'wkt': 'POINT(37.5648 55.7558)'}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs['wkt'])
    folium.Marker([point.y, point.x], popup=obs['date']).add_to(m)

# Сохранение карты
m.save("205.html")