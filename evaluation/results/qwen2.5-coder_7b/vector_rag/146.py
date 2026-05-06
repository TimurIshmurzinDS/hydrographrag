import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для контекста)
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

# Координаты датчиков (пример)
sensor_locations = [
    {'name': 'Датчик Аягоз', 'geometry': wkt.loads('POINT(37.123456 40.987654)')},
    {'name': 'Датчик Токыраун', 'geometry': wkt.loads('POINT(38.123456 41.987654)')}
]

# Добавление датчиков на карту
for sensor in sensor_locations:
    folium.Marker(
        location=[sensor['geometry'].y, sensor['geometry'].x],
        popup=sensor['name'],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("146.html")