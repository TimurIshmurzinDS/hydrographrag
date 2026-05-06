import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='basin', 
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 74.5678},
    {'lat': 43.2345, 'lon': 75.6789}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], 
                  popup='Координаты: {} {}'.format(coord['lat'], coord['lon'])).add_to(m)

# Сохранение карты в файл
m.save("58.html")