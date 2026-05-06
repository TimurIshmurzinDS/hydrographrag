import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре массы геоданных
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка координат пойменных земель (если они есть)
# Пример:
# coordinates = [
#     {'name': 'Пойменная земля 1', 'geometry': wkt.loads('POINT(123.456 78.901)')},
#     {'name': 'Пойменная земля 2', 'geometry': wkt.loads('POINT(124.456 79.901)')}
# ]

# Добавление пойменных земель на карту
# for coord in coordinates:
#     folium.Marker([coord['geometry'].y, coord['geometry'].x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("184.html")