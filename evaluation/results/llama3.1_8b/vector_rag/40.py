import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек с координатами (WKT)
points = [
    {'name': 'Талгар', 'location': wkt.loads('POINT(76.9333 43.0333)')},
    {'name': 'г. Талгар', 'location': wkt.loads('POINT(76.9334 43.0334)')},
    {'name': 'г. Талгар', 'location': wkt.loads('POINT(76.9335 43.0335)')}
]

# Добавление точек на карту
for point in points:
    folium.Marker(point['location'].coords[0], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("40.html")