import geopandas as gpd
from shapely.geometry import shape
import networkx as nx
import folium

# Загрузите данные о реках в формате GeoJSON
river1 = gpd.read_file('ulken_almaty.geojson')
river2 = gpd.read_file('shyzyn.geojson')

# Создайте графики потоков для каждой реки
G1 = nx.Graph()
for i, row in river1.iterrows():
    geom = shape(row.geometry)
    for j in range(i+1, len(river1)):
        geom2 = shape(river1.iloc[j].geometry)
        if geom.intersects(geom2):
            G1.add_edge(i, j)

G2 = nx.Graph()
for i, row in river2.iterrows():
    geom = shape(row.geometry)
    for j in range(i+1, len(river2)):
        geom2 = shape(river2.iloc[j].geometry)
        if geom.intersects(geom2):
            G2.add_edge(i, j)

# Объедините графики потоков и найдите общую вершину
G = nx.compose(G1, G2)
common_node = None
for node in G.nodes():
    if G1.has_node(node) and G2.has_node(node):
        common_node = node
        break

# Если существует общая вершина, то реки связаны через систему притоков
if common_node is not None:
    print("Реки связаны через систему притоков.")
else:
    print("Реки не связаны через систему притоков.")

# Визуализируйте графики потоков на карте
m = folium.Map(location=[43.25, 76.95], zoom_start=10)
folium.Polygon(river1.geometry.unary_union.exterior.coords[:], color='blue').add_to(m)
folium.Polygon(river2.geometry.unary_union.exterior.coords[:], color='red').add_to(m)

# Нарисуйте графики потоков на карте
for edge in G.edges():
    if G1.has_edge(edge[0], edge[1]):
        folium.PolyLine([(river1.iloc[edge[0]].geometry.centroid.x, river1.iloc[edge[0]].geometry.centroid.y),
                         (river1.iloc[edge[1]].geometry.centroid.x, river1.iloc[edge[1]].geometry.centroid.y)],
                        color='blue').add_to(m)
    if G2.has_edge(edge[0], edge[1]):
        folium.PolyLine([(river2.iloc[edge[0]].geometry.centroid.x, river2.iloc[edge[0]].geometry.centroid.y),
                         (river2.iloc[edge[1]].geometry.centroid.x, river2.iloc[edge[1]].geometry.centroid.y)],
                        color='red').add_to(m)

# Сохраните карту в файл
m.save("95.html")