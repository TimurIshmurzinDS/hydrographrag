import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для демонстрации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат притоков (если они доступны)
prickly_points = [
    {'name': 'Lepsy River', 'wkt': 'POINT(37.123456 48.987654)'},
    {'name': 'Shilik River', 'wkt': 'POINT(37.567890 49.123456)'}
]

# Добавление точек притоков на карту
for point in prickly_points:
    folium.Marker(
        location=[point['wkt'].split(' ')[1], point['wkt'].split(' ')[2]],
        popup=point['name'],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("152.html")