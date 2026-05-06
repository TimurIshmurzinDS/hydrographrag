import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT) рек
wkt_coords = [
    {"name": "Узень Каргалы", "coords": wkt.loads("POINT(46.1234 60.5678)")},
    {"name": "Быжый", "coords": wkt.loads("POINT(47.9012 61.2345)")},
    {"name": "Шижин", "coords": wkt.loads("POINT(48.3456 62.4567)")}
]

# Добавление маркеров на карту
for river in wkt_coords:
    folium.Marker(location=river["coords"].coords[0], popup=river["name"]).add_to(m)

# Сохранение карты в файл
m.save("219.html")