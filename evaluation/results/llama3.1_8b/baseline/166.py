import geopandas as gpd
from networkx import DiGraph, connected_components
from networkx.algorithms.centrality import centrality_centrals
from folium import Map, Marker

# Шаг 1: Загрузите данные о притоках реки Талгар
gdf = gpd.read_file('path/to/TalgarRiver.shp')

# Шаг 2: Создайте граф, представляющий структуру притоков реки Талгар
G = DiGraph()
for index, row in gdf.iterrows():
    G.add_node(row['name'])
    if 'upstream' in row:
        G.add_edge(row['name'], row['upstream'])

# Шаг 3: Используйте алгоритм нахождения центростремительных компонентов (CC) для определения основных узлов слияния
cc = connected_components(G)
main_nodes = []
for component in cc:
    if len(component) > 5:  # Установите пороговое значение, чтобы определить основные узлы слияния
        main_nodes.extend(component)

# Шаг 4: Визуализируйте результаты на карте
m = Map(location=[43.0, 76.7], zoom_start=10)
for node in main_nodes:
    marker = Marker(location=gdf[gdf['name'] == node].geometry.centroid.values[0],
                    popup=node,
                    icon=None).add_to(m)

# Сохраните карту в файл
m.save("166.html")