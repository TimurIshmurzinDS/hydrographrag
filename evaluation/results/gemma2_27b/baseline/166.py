import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
import folium

# Загрузка данных о реке из файла (формат GeoJSON)
river_data = gpd.read_file("talgar_river.geojson")

# Создание графа
G = nx.DiGraph()

# Добавление узлов и дуг в граф
for index, row in river_data.iterrows():
    # Узлы - точки слияния рек
    node = Point(row.geometry.x, row.geometry.y)
    G.add_node(node)

    # Дуги - русла рек
    for neighbor in row.neighbors:
        neighbor_node = Point(neighbor.geometry.x, neighbor.geometry.y)
        G.add_edge(node, neighbor_node)

# Поиск узлов с максимальным количеством соединений (узлы слияния)
nodes_with_max_connections = [node for node in G.nodes() if len(list(G.neighbors(node))) > 1]

# Визуализация на карте
m = folium.Map(location=[river_data.geometry.y, river_data.geometry.x], zoom_start=12)

for node in nodes_with_max_connections:
    folium.Marker(location=[node.y, node.x]).add_to(m)

# Сохранение карты
m.save("166.html")