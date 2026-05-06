import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.unary_union.__geo_interface__, name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты WKT, создаем список словарей
wkt_coordinates = [
    {"lat": 37.7749, "lon": -122.4194},
    {"lat": 38.8977, "lon": -77.0365}
]

# Добавление маркеров на карту
for coord in wkt_coordinates:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Технологический сектор').add_to(m)

# Сохранение карты в файл
m.save("277.html")