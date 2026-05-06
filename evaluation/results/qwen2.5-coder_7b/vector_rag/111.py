import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты наблюдений для Temirlik village (пример)
temirlik_village_coords = [
    {'name': 'Temirlik village 1', 'wkt': 'POINT(45.1234 38.9012)'},
    {'name': 'Temirlik village 2', 'wkt': 'POINT(45.1235 38.9013)'},
    {'name': 'Temirlik village 3', 'wkt': 'POINT(45.1236 38.9014)'}
]

# Преобразование WKT в объекты Shapely
temirlik_village_points = [wkt.loads(coord['wkt']) for coord in temirlik_village_coords]

# Добавление точек наблюдений на карту
for point in temirlik_village_points:
    folium.Marker([point.y, point.x], popup='Temirlik village').add_to(m)

# Сохранение карты в файл
m.save("111.html")