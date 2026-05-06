import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузите данные о реках и датчиках
rivers_gdf = gpd.read_file('path/to/rivers.shp')
sensors_gdf = gpd.read_file('path/to/sensors.shp')

# Определите порог расстояния для технического обслуживания
distance_threshold = 10

# Создайте функцию для определения необходимости технического обслуживания
def needs_maintenance(sensor):
    # Получите ближайший участок реки к датчику
    nearest_river = rivers_gdf.nearest([sensor.geometry])[0]
    
    # Определите расстояние между датчиком и рекой
    distance = sensor.geometry.distance(nearest_river.geometry)
    
    return distance > distance_threshold

# Примените функцию к каждому датчику
sensors_gdf['needs_maintenance'] = sensors_gdf.apply(needs_maintenance, axis=1)

# Визуализируйте результаты на карте
m = folium.Map(location=[46.5, 58.0], zoom_start=8)
folium.Choropleth(
    geo_data=sensors_gdf,
    name='needs_maintenance',
    data=sensors_gdf,
    columns=['geometry', 'needs_maintenance'],
    key_on='feature.properties.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

# Сохраните карту в файл
m.save("146.html")