import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о топологии сети (пример: shapefile)
network_gdf = gpd.read_file('path_to_your_network_shapefile.shp')

# Идентификация узлов и ребер
nodes = network_gdf[network_gdf['geometry'].type == 'Point']
edges = network_gdf[network_gdf['geometry'].type == 'LineString']

# Определение направления потока от реки Шынжалы к основным речным системам
source_node = nodes[nodes['name'] == 'Шынжалы'].iloc[0]
target_nodes = nodes[nodes['category'] == 'Основные речные системы']

# Используем алгоритм поиска кратчайшего пути (например, Dijkstra)
from networkx import Graph, from_networkx

G = from_networkx(edges.to_crs(epsg=4326), edge_attr='length')
source_point = source_node.geometry
target_points = target_nodes.geometry

# Найдем кратчайший путь от Шынжалы до каждой из основных речных систем
paths = {}
for target_point in target_points:
    path = nx.shortest_path(G, source=source_point, target=target_point, weight='length')
    paths[target_point] = path

# Визуализация результатов на карте
m = folium.Map(location=[nodes['geometry'].y.mean(), nodes['geometry'].x.mean()], zoom_start=10)

for edge in edges.itertuples():
    if isinstance(edge.geometry, LineString):
        folium.PolyLine(locations=edge.geometry.coords, color='blue', weight=2).add_to(m)

for node in nodes.itertuples():
    folium.Marker(location=[node.geometry.y, node.geometry.x], popup=node.name, icon=folium.Icon(color='red')).add_to(m)

# Добавление направлений потока
for target_point, path in paths.items():
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        folium.PolyLine(locations=[start.coords[0], end.coords[0]], color='green', weight=2).add_to(m)

m.save("173.html")