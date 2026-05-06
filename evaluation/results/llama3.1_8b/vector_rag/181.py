import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.__geo_interface__,
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек с координатами WKT
wkt_points = [
    {"name": "Точка 1", "geometry": wkt.loads("POINT(48.6784 18.4235)")},
    {"name": "Точка 2", "geometry": wkt.loads("POINT(48.6793 18.4246)")},
]

# Добавление точек на карту
for point in wkt_points:
    folium.Marker(point["geometry"].coords, popup=point["name"]).add_to(m)

# Сохранение карты в файл
m.save("181.html")