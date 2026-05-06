import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с географическими границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре геометрии бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат для отметок уровня воды (если они есть)
water_level_markers = [
    {'location': [41.35, 76.9], 'tooltip': 'Уровень воды: 100 м'},
    {'location': [41.36, 76.92], 'tooltip': 'Уровень воды: 110 м'}
]

# Добавление отметок уровня воды на карту
for marker in water_level_markers:
    folium.Marker(location=marker['location'], tooltip=marker['tooltip']).add_to(m)

# Сохранение карты в файл
m.save("237.html")