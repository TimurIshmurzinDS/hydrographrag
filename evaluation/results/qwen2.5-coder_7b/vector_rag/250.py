import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о топографической сети притоков реки Тентек
basin_data = r"data/basin_data.shp"
gdf = gpd.read_file(basin_data)
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в centroid базина
centroid = gdf.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление базина на карту
folium.GeoJson(gdf.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка координат узлов топографической сети (пример)
nodes = [
    {'name': 'Node1', 'wkt': 'POINT(37.5648 55.7558)'},
    {'name': 'Node2', 'wkt': 'POINT(37.5649 55.7559)'},
    {'name': 'Node3', 'wkt': 'POINT(37.5650 55.7560)'}
]

# Преобразование WKT в координаты
node_coords = [(wkt.loads(node['wkt']).x, wkt.loads(node['wkt']).y) for node in nodes]

# Добавление узлов на карту
for coord in node_coords:
    folium.Marker(coord, popup='Node').add_to(m)

# Сохранение карты в файл
m.save("250.html")