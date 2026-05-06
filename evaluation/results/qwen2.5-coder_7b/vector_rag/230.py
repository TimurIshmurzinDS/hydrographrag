import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile и использованием тайлов 'CartoDB positron'
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Если в контексте есть координаты (WKT), создаем список словарей с координатами
coordinates = [
    {'name': 'Observation 1', 'wkt': 'POINT(37.422 -122.084)'},
    {'name': 'Observation 2', 'wkt': 'POINT(37.425 -122.086)'},
    {'name': 'Observation 3', 'wkt': 'POINT(37.427 -122.088)'},
    {'name': 'Observation 4', 'wkt': 'POINT(37.429 -122.090)'}
]

# Преобразование WKT в координаты
coordinates_list = [(wkt.loads(coord['wkt']).x, wkt.loads(coord['wkt']).y) for coord in coordinates]

# Добавление точек наблюдений на карту
for coord in coordinates_list:
    folium.Marker(coord).add_to(m)

# Сохранение карты в файл "230.html"
m.save("230.html")