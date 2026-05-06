import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейнах
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна
centroid = gdf.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.__geo_interface__,
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coords = [
    {"name": "Урзхар", "coords": wkt.loads("POINT(75.1234 46.5678)")},
    {"name": "Шарын", "coords": wkt.loads("POINT(76.9012 47.2345)")}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord["coords"].y, coord["coords"].x], popup=coord["name"]).add_to(m)

# Сохранение карты в файл
m.save("188.html")