import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты точек наблюдений для рек Koksu и Byzhy в формате WKT
# Создание списка словарей с координатами и названиями рек
observation_points = [
    {'name': 'Koksu River', 'wkt': 'POINT(78.5 42.6)'},
    {'name': 'Byzhy River', 'wkt': 'POINT(79.0 43.1)'}
]

# Добавление точек наблюдений на карту
for point in observation_points:
    geom = wkt.loads(point['wkt'])
    folium.Marker([geom.y, geom.x], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("208.html")