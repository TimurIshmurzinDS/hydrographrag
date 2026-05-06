import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту как GeoJSON
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей с координатами (WKT) рек
coordinates = [
    {"name": "Река Каратал", "wkt": wkt.loads("POINT(75.1234 46.5678)")},
    {"name": "Река Коктал", "wkt": wkt.loads("POINT(76.9012 45.4321)")},
    {"name": "Река Баянколь", "wkt": wkt.loads("POINT(77.6543 44.1098)")},
    {"name": "Река Карой", "wkt": wkt.loads("POINT(78.3214 43.7654)")},
]

# Добавить координаты на карту
for coord in coordinates:
    folium.Marker(coord["wkt"].coords, popup=coord["name"]).add_to(m)

# Сохранить карту в файл
m.save("214.html")