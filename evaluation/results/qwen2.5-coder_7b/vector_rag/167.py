import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассина
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат узлов и участков речной сети (WKT)
nodes = [
    {'name': 'Node1', 'geometry': wkt.loads('POINT(35.1234 46.7890)')},
    {'name': 'Node2', 'geometry': wkt.loads('POINT(35.2345 46.8901)')},
    {'name': 'Node3', 'geometry': wkt.loads('POINT(35.3456 46.9012)')}
]

edges = [
    {'start_node': 'Node1', 'end_node': 'Node2', 'length': 10},  # Пример длины участка
    {'start_node': 'Node2', 'end_node': 'Node3', 'length': 15}
]

# Создание графа речной сети
import networkx as nx

G = nx.Graph()
for node in nodes:
    G.add_node(node['name'], pos=(node['geometry'].y, node['geometry'].x))

for edge in edges:
    start_node = edge['start_node']
    end_node = edge['end_node']
    length = edge['length']
    G.add_edge(start_node, end_node, weight=length)

# Расчет общей протяженности пути от одной точки до другой
start_point = 'Node1'
end_point = 'Node3'

path_length = nx.shortest_path_length(G, source=start_point, target=end_point, weight='weight')
print(f"Общая протяженность пути от {start_point} до {end_point}: {path_length}")

# Визуализация речной сети и путей на карте
for edge in edges:
    start_node = edge['start_node']
    end_node = edge['end_node']
    start_pos = G.nodes[start_node]['pos']
    end_pos = G.nodes[end_node]['pos']
    folium.PolyLine([start_pos, end_pos], color='blue', weight=2.5).add_to(m)

# Сохранение карты
m.save("167.html")