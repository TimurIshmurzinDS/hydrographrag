import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна реки Бутак
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Если в контексте есть координаты (WKT), создаем список словарей с координатами
coordinates = [
    {'name': 'Butak village', 'geometry': wkt.loads('POINT(37.12345 55.67890)')},
    {'name': 'Butak village', 'geometry': wkt.loads('POINT(37.12345 55.67890)')},
    {'name': 'Butak village', 'geometry': wkt.loads('POINT(37.12345 55.67890)')},
    {'name': 'Butak village', 'geometry': wkt.loads('POINT(37.12345 55.67890)')}
]

# Добавление точек на карту
for coord in coordinates:
    folium.Marker([coord['geometry'].y, coord['geometry'].x], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("192.html")