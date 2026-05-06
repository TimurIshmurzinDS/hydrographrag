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

# Координаты притоков реки Тентек (пример данных)
prongs = [
    {'name': 'Tekes River', 'wkt': 'POINT(35.1234 46.7890)'},
    {'name': 'Temirlik River', 'wkt': 'POINT(36.1234 47.7890)'},
    {'name': 'Tekeli River', 'wkt': 'POINT(37.1234 48.7890)'}
]

# Добавление притоков на карту
for prong in prongs:
    point = wkt.loads(prong['wkt'])
    folium.Marker([point.y, point.x], popup=prong['name'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("178.html")