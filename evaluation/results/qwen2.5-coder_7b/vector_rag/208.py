import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с географическими границами бассейнов
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid shapefile и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление географических границ бассейнов на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат точек для отслеживания уровня воды (замените на реальные данные)
coordinates = [
    {'name': 'Koksu River', 'wkt': 'POINT(45.1234 78.9012)'},
    {'name': 'Byzhy River', 'wkt': 'POINT(46.5678 79.0123)'}
]

# Преобразование WKT в объекты Shapely
points = [wkt.loads(coord['wkt']) for coord in coordinates]

# Добавление точек на карту
for point, coord in zip(points, coordinates):
    folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("208.html")