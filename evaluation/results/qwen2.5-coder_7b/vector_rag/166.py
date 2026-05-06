import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна и заданием стиля
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат узлов слияния (если они есть в контексте)
# В реальном случае эти данные должны быть получены из других источников
merge_points = [
    {'name': 'Узел 1', 'geometry': wkt.loads('POINT(45.0 30.0)')},
    {'name': 'Узел 2', 'geometry': wkt.loads('POINT(46.0 31.0)')}
]

# Добавление узлов слияния на карту
for point in merge_points:
    folium.Marker([point['geometry'].y, point['geometry'].x], popup=point['name'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("166.html")