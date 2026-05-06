import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Создание карты с использованием центроида водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты точки наблюдения в формате WKT
# В данном примере создадим точку с координатами (56.1374, 40.4079) как пример
observation_points = [
    {'name': 'Наблюдательная точка', 'wkt': 'POINT(40.4079 56.1374)', 'level': 123.45}  # Примерные координаты и уровень воды
]

# Добавление точек наблюдения на карту
for point in observation_points:
    geom = wkt.loads(point['wkt'])
    folium.Marker(
        location=[geom.y, geom.x],
        popup=f"Точка: {point['name']}\nУровень воды: {point['level']} м",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("5.html")