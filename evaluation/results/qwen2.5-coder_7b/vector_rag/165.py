import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат для демонстрации (замените на реальные данные)
coordinates = [
    {'name': 'Shyzhyn River', 'wkt': 'POINT(75.1234 45.6789)'},
    {'name': 'Sarykan River', 'wkt': 'POINT(76.1234 46.6789)'}
]

# Добавление точек с уровнями воды на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=f"{coord['name']} - Уровень воды: {Water_level_Value} м").add_to(m)

# Сохранение карты в файл
m.save("165.html")