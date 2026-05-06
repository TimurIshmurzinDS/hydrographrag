import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Aksu River из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid shapefile и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы реки на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о датчиках уровня воды (если доступны)
sensor_data = [
    {'name': 'Sensor_1', 'geometry': wkt.loads('POINT(37.5 42)'), 'water_level': 150},
    {'name': 'Sensor_2', 'geometry': wkt.loads('POINT(38.0 42.5)'), 'water_level': 160}
]

# Добавление датчиков на карту
for sensor in sensor_data:
    folium.Marker(
        location=[sensor['geometry'].y, sensor['geometry'].x],
        popup=f"{sensor['name']}: Уровень воды - {sensor['water_level']} см",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("61.html")