import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами реки Karatal River
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в геометрии реки
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы реки на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных уровня воды (если доступны)
water_level_data = [
    {'name': 'Sensor1', 'geometry': wkt.loads('POINT(39.5678 40.1234)'), 'value': 150},
    {'name': 'Sensor2', 'geometry': wkt.loads('POINT(39.6789 40.2345)'), 'value': 160}
]

# Добавление данных уровня воды на карту
for sensor in water_level_data:
    folium.Marker(
        location=[sensor['geometry'].y, sensor['geometry'].x],
        popup=f"{sensor['name']}: {sensor['value']} см",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("2.html")