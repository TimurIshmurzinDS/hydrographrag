import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid базина и тайлами CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление базина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат притоков (если они известны)
prickly_points = [
    {'name': 'Prickly Point 1', 'geometry': wkt.loads('POINT(45.1234 67.5678)')},
    {'name': 'Prickly Point 2', 'geometry': wkt.loads('POINT(45.9012 67.3456)')}
]

# Добавление притоков на карту
for point in prickly_points:
    folium.Marker([point['geometry'].y, point['geometry'].x], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("91.html")