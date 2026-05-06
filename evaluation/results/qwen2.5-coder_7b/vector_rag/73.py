import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка координат датчиков уровня воды
sensor_locations = [
    {'name': 'Osek River', 'geometry': wkt.loads('POINT(10.5 48.3)')},
    {'name': 'Koktal River', 'geometry': wkt.loads('POINT(12.7 49.1)')}
]

# Добавление маркеров датчиков уровня воды на карту
for sensor in sensor_locations:
    folium.Marker(
        location=[sensor['geometry'].y, sensor['geometry'].x],
        popup=f"Датчик уровня воды: {sensor['name']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("73.html")