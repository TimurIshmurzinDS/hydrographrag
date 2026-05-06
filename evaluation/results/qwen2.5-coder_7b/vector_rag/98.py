import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в centroid бассейнов
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат рек (если они доступны)
rivers = [
    {'name': 'Tentek River', 'wkt': 'POINT(37.5 -122.4)'},
    {'name': 'Byzhy River', 'wkt': 'POINT(38.0 -122.6)'}
]

# Добавление рек на карту
for river in rivers:
    point = wkt.loads(river['wkt'])
    folium.Marker([point.y, point.x], popup=river['name']).add_to(m)

# Сохранение карты
m.save("98.html")