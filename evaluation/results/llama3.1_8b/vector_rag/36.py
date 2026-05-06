import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек с координатами (WKT)
points = [
    {"name": "Шынжалы", "geometry": wkt.loads("POINT(48.6784 69.3245)")},
    {"name": "Шызгин", "geometry": wkt.loads("POINT(49.1231 70.4567)")},
    {"name": "Баянколь", "geometry": wkt.loads("POINT(47.8901 68.2345)")},
]

# Добавление точек на карту
for point in points:
    folium.Marker(point["geometry"].coords, popup=point["name"]).add_to(m)

# Сохранение карты в файл
m.save("36.html")