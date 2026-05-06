import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Koktal River из shapefile
koktal_river = gpd.read_file(r"data/basin_data.shp")
koktal_river = koktal_river.to_crs('EPSG:4326')

# Создание карты с центром в centroid shapefile и параметрами tiles='CartoDB positron'
centroid = koktal_river.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление реки на карту
folium.GeoJson(koktal_river.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о точках мониторинга и уровнях воды (замените на реальные данные)
monitoring_points = [
    {'name': 'Point1', 'geometry': wkt.loads('POINT(37.5648 40.9234)'), 'water_level': 150},
    {'name': 'Point2', 'geometry': wkt.loads('POINT(37.5748 40.9334)'), 'water_level': 160}
]

# Добавление точек мониторинга и уровней воды на карту
for point in monitoring_points:
    folium.Marker(
        location=[point['geometry'].y, point['geometry'].x],
        popup=f"{point['name']}: Уровень воды - {point['water_level']} см",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("88.html")