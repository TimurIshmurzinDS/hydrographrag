import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре масс бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты наблюдений (WKT)
observations = [
    {'wkt': 'POINT(35.1234 46.7890)', 'label': 'Observation 1'},
    {'wkt': 'POINT(35.2345 46.8901)', 'label': 'Observation 2'},
    {'wkt': 'POINT(35.3456 46.9012)', 'label': 'Observation 3'},
    {'wkt': 'POINT(35.4567 46.0123)', 'label': 'Observation 4'}
]

# Преобразование координат WKT в геометрии и добавление на карту
for obs in observations:
    geom = wkt.loads(obs['wkt'])
    folium.Marker([geom.y, geom.x], popup=obs['label']).add_to(m)

# Сохранение карты
m.save("172.html")