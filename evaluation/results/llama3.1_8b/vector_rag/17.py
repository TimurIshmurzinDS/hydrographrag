import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 79.5678},
    {'lat': 43.2345, 'lon': 80.0123},
    # Добавьте остальные координаты в этот список
]

# Создание карты с маркерами для координат (WKT)
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Координата').add_to(m)

# Сохранение карты в файл
m.save("17.html")