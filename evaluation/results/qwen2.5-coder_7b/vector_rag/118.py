import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты виллы Temirlik (пример)
temirlik_village_coords = [
    {'name': 'Temirlik village', 'geometry': wkt.loads('POINT(73.123456 42.789012)')}
]

# Добавление координат виллы на карту
for point in temirlik_village_coords:
    folium.Marker([point['geometry'].y, point['geometry'].x], popup=point['name']).add_to(m)

# Сохранение карты
m.save("118.html")