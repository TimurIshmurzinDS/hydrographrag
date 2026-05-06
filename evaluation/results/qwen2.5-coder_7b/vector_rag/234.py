import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат для сезонного разлива реки Шарын (замените на реальные данные)
seasonal_diversion = [
    {'name': 'Seasonal Diversion', 'geometry': wkt.loads('POINT(45.123 67.456)')}
]

# Добавление точки сезонного разлива на карту
for diversion in seasonal_diversion:
    folium.Marker(
        location=[diversion['geometry'].y, diversion['geometry'].x],
        popup=diversion['name'],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты в файл
m.save("234.html")