import geopandas as gpd
import folium
from shapely import wkt

# Загрузка и преобразование данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на бассейне
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных датчиков (если они есть)
sensor_data = [
    {'name': 'Sensor1', 'geometry': wkt.loads('POINT(37.422 -122.084)'), 'value': 50, 'classification': 'Low'},
    {'name': 'Sensor2', 'geometry': wkt.loads('POINT(37.425 -122.086)'), 'value': 100, 'classification': 'Medium'}
]

# Добавление данных датчиков на карту
for sensor in sensor_data:
    folium.Marker(
        location=[sensor['geometry'].y, sensor['geometry'].x],
        popup=f"Sensor: {sensor['name']}, Value: {sensor['value']} cm, Classification: {sensor['classification']}",
        icon=folium.Icon(color='red' if sensor['classification'] == 'High' else 'green')
    ).add_to(m)

# Сохранение финальной карты
m.save("145.html")