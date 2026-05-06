import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Bassin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT) для реки Талгар
talgar_river_wkt = [
    {"name": "Talgar River", "wkt": "POINT(76.6667 43.0333)"},
    # Добавьте остальные точки вручную, если они есть
]

# Создание карты с координатами (WKT) для реки Талгар
for point in talgar_river_wkt:
    folium.Marker(location=wkt.loads(point['wkt']).coords[0], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("3.html")