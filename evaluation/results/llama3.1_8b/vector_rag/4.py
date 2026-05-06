import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coords = [
    {'name': 'Koktal River', 'coords': wkt.loads('POINT(48.123 69.456)')},
    {'name': 'Koksu River', 'coords': wkt.loads('POINT(50.789 70.321)')},
    {'name': 'Karatal River', 'coords': wkt.loads('POINT(46.543 68.901)')},
    {'name': 'Bayankol River', 'coords': wkt.loads('POINT(47.987 69.654)')},
    {'name': 'Butak River', 'coords': wkt.loads('POINT(49.321 70.789)')}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker(location=coord['coords'].coords[0], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("4.html")