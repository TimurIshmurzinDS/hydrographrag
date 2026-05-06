import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt),
               name='Basin',
               style_function=lambda feature: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coordinates = [
    {"lat": 55.7558, "lon": 37.6173},
    {"lat": 40.7128, "lon": -74.0060},
    {"lat": 34.0522, "lon": -118.2437}
]

# Добавление маркеров на карту
for coordinate in wkt_coordinates:
    folium.Marker([coordinate['lat'], coordinate['lon']], popup='Маркер').add_to(m)

# Сохранение карты в файл
m.save("275.html")