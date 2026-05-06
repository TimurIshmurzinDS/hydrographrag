import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point
import folium

# Загрузить данные о речной сети
rivers = gpd.read_file("rivers.shp")

# Создать граф из речной сети
G = nx.Graph()
for index, row in rivers.iterrows():
    G.add_node(index)
    for neighbor in rivers[rivers.intersects(row.geometry)].index:
        if neighbor != index:
            G.add_edge(index, neighbor)

# Найти узлы устьев притоков Тентек
tentek_tributaries = [index for index, row in rivers.iterrows() if "Тентек" in row["NAME"]]

# Анализ топологии вокруг узлов устьев

for tributary in tentek_tributaries:
    print(f"Узел {tributary}:")
    print(f"Количество приходящих ребер: {G.degree(tributary)}")
    print(f"Расстояние до других узлов:")
    for neighbor in G.neighbors(tributary):
        print(f"\t{neighbor}: {nx.shortest_path_length(G, source=tributary, target=neighbor)} ребер")

# Визуализация

m = folium.Map(location=[rivers.geometry.y.mean(), rivers.geometry.x.mean()], zoom_start=10)
for index, row in rivers.iterrows():
    folium.GeoJson(row.geometry).add_to(m)

# Выделить узлы устьев притоков Тентек другим цветом

for tributary in tentek_tributaries:
    folium.Circle(location=rivers.loc[tributary].geometry.centroid, radius=50, color="red").add_to(m)

m.save("178.html")