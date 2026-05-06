import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре масс бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о показаниях датчиков Dos River (замените на реальные данные)
sensor_data = [
    {'name': 'Sensor1', 'location': wkt.loads('POINT(37.422 -122.084)'), 'water_level': 50},
    {'name': 'Sensor2', 'location': wkt.loads('POINT(37.423 -122.085)'), 'water_level': 60}
]

# Добавление точек с показаниями датчиков на карту
for sensor in sensor_data:
    folium.Marker(
        location=[sensor['location'].y, sensor['location'].x],
        popup=f"{sensor['name']}: {sensor['water_level']} см",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("213.html")