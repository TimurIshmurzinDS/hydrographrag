import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты Марса с указанием изменений водяного уровня в различных регионах
m = folium.Map(location=basin_data.centroid, zoom_start=4, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt),
               name='Basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coords = [
    {'lat': 45.5236, 'lon': -122.6750},
    {'lat': 37.7749, 'lon': -122.4194}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Наблюдение').add_to(m)

# Сохранение карты в файл
m.save("284.html")