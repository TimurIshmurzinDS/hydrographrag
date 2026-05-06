import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.__geo_interface__,
               name='Basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек с координатами
points = [
    {'location': [55.123, 37.456], 'popup': 'Точка 1'},
    {'location': [55.789, 38.901], 'popup': 'Точка 2'}
]

# Добавление точек на карту
for point in points:
    folium.Marker(point['location'], popup=point['popup']).add_to(m)

# Сохранение карты в файл
m.save("243.html")