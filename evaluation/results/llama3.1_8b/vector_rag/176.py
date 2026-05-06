import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_gdf.to_json(), name='бассейн').add_to(m)

# Создание списка точек с координатами WKT
points = [
    {'location': wkt.loads('POINT(76.9333 42.9667)')},
    {'location': wkt.loads('POINT(76.9167 42.9833)')},
    {'location': wkt.loads('POINT(76.9000 43.0000)')},
    {'location': wkt.loads('POINT(76.8833 43.0167)')}
]

# Добавление точек на карту
for point in points:
    folium.Marker(location=point['location'].coords[0], popup='Талгар').add_to(m)

# Создание списка точек с координатами русла ручья Терисбутак
terisbuthak_points = [
    {'location': wkt.loads('POINT(76.9333 42.9667)')},
    {'location': wkt.loads('POINT(76.9167 42.9833)')},
    {'location': wkt.loads('POINT(76.9000 43.0000)')},
    {'location': wkt.loads('POINT(76.8833 43.0167)')}
]

# Добавление точек на карту
for point in terisbuthak_points:
    folium.Marker(location=point['location'].coords[0], popup='Ручей Терисбутак').add_to(m)

# Сохранение карты в файл
m.save("176.html")