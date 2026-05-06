import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.exterior), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если в контексте есть координаты WKT, создаем список словарей для добавления на карту
wkt_coords = [
    {"lat": 43.1234, "lon": 79.5678},
    {"lat": 42.9011, "lon": 78.3456}
]

# Добавление координат на карту
for coord in wkt_coords:
    folium.CircleMarker([coord['lat'], coord['lon']], radius=5).add_to(m)

# Сохранение карты в файл
m.save("161.html")