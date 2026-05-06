import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты ручных точек (если есть)
# Пример: hardcoded list of dictionaries
observation_points = [
    {"name": "Observation_2284", "geometry": wkt.loads("POINT(51.5074 -0.1278)")},
    {"name": "Observation_2219", "geometry": wkt.loads("POINT(51.5074 -0.1278)"})
]

# Добавление ручных точек на карту
for point in observation_points:
    folium.Marker([point['geometry'].y, point['geometry'].x], popup=point['name']).add_to(m)

# Сохранение карты
m.save("159.html")