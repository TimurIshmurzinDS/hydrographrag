import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка shapefile с данными бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# 3. Добавление бассейна на карту как GeoJSON
folium.GeoJson(data=basin_data.to_crs(epsg=4326).geometry.__geo_interface__,
               name='Бассейн',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Если в контексте есть координаты WKT, создаем список словарей
wkt_coordinates = [
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.987654, 'lon': 77.321098}
]

# 5. Добавление маркеров на карту с координатами WKT
for coord in wkt_coordinates:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Маркер').add_to(m)

# 6. Сохранение карты в файл html
m.save("237.html")